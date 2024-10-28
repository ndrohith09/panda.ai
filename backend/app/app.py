from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig 
from starlette.responses import JSONResponse 
import uvicorn
from fastapi.middleware.cors import CORSMiddleware 
import uuid, json
from tools import debug_apache_error_log, debug_linux_error_log, debug_zookeeper_error_log 
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import *
from email_template import draft_email_format
import asyncpg, re
from schema import PostSchema, EmailSchema, LLMSchema,UserLoginSchema, LogRequestSchema, UserSchema, TeamSchema
from fastapi import FastAPI, BackgroundTasks
from polling import poll_endpoint
from dotenv import load_dotenv
import os

from auth.auth_bearer import JWTBearer
from auth.auth_handler import get_password_hash , signJWT , verify_password

load_dotenv()

async def startup_event():
    app.state.db = await asyncpg.create_pool(
        host=os.getenv('PG_HOST'),
        database=os.getenv('PG_DATABASE'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PWD')
    )
    await create_table_if_not_exists(app.state.db)
    print("connected", app.state.db)

async def shutdown_event():
    await app.state.db.close()

app = FastAPI(
    on_startup=[startup_event, ],
    # on_startup=[startup_event, start_polling],
    on_shutdown=[shutdown_event],
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def create_table_if_not_exists(db):
    
    create_pipeline_table = """
    CREATE TABLE IF NOT EXISTS pipeline (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255),
        connection VARCHAR(255),
        status VARCHAR(50)
    );
    """

    create_logs_table = """
    CREATE TABLE IF NOT EXISTS logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notify_team BOOLEAN,
    team_members TEXT[] DEFAULT TEXT::JSONB[],  
    logs JSONB[] DEFAULT ARRAY[]::JSONB[],
    pipeline_id UUID,
    FOREIGN KEY (pipeline_id) REFERENCES pipeline(id) 
    );
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    );
    """
    try:
        async with db.acquire() as connection:
            await connection.execute(create_pipeline_table)
            await connection.execute(create_logs_table)
            await connection.execute(create_table_query)
        print("Table created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

tools = [debug_apache_error_log, debug_zookeeper_error_log, debug_linux_error_log]

system_prompt = """
    You are an agent responsible for debugging error logs and mail them to Respective Mail Id.

    You are provided with several functions (tools) and must choose and fill their parameters based on the given situation.

    When presented with a error log, select the appropriate function to solve it.

    The Functions provided to you are:

    {{SUPPORTED_TOOLS_FUNCTIONS}}

    Our task is to analyze the error, and provide a solution returned from the function tool.

    Output format:  `Solution: <solution_returned_from_function_tool>` or a status if the operation is not supported.

    Examples:

    Input : Apache Error Log Format: [Time], [Level], Content - [Sun Dec 04 04:47:44 2005] [error] mod_jk child workerEnv in error state 6

    Once you receive the [Event Id] and [Event Template] from tool, analyse the error log and provide a proper solution
    
    Solution: <your_analysis_on_solution_returned_from_function_tool>

    """

llm = ChatOpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',
    model="llama3.2"
)  

llm_agent = create_react_agent(llm, tools=tools, state_modifier=system_prompt)

conf = ConnectionConfig(
    MAIL_USERNAME = "abc@gmail.com",
    MAIL_FROM = "abc@gmail.com",
    MAIL_PASSWORD = "***",
    MAIL_FROM_NAME="AI Agent",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)    
     

@app.post("/start-polling/" ,
        #   dependencies=[Depends(JWTBearer())]
          )
async def start_polling(url: str, interval: int = 5, background_tasks: BackgroundTasks = None):
    """
    Starts polling an endpoint at the specified interval.
    - `url`: URL of the endpoint to poll.
    - `interval`: Time interval between polls (in seconds).
    """
    background_tasks.add_task(poll_endpoint, url, interval)
    return {"message": "Polling started", "url": url, "interval": interval}


@app.get("/pipeline",
        #   dependencies=[Depends(JWTBearer())]
         )
async def get_pipeline():
    query = "SELECT * FROM pipeline"
    try:
      async with app.state.db.acquire() as connection:
          rows = await connection.fetch(query) 
      pipelines = [{key: (str(value) if isinstance(value, uuid.UUID) else value) for key, value in dict(row).items()} for row in rows]

      return JSONResponse(status_code=200, content={"pipelines": pipelines})
    except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error{e}")


@app.post("/pipeline/create",
        #   dependencies=[Depends(JWTBearer())]
          )
async def create_pipeline(pipeline : PostSchema = Body(...)): 
    create_pipeline_query = """
        INSERT INTO pipeline (name, connection, status)
        VALUES ($1, $2, $3)
        RETURNING id;
        """
    
    create_log_query = """
        INSERT INTO logs (notify_team, team_members, logs, pipeline_id)
        VALUES ($1, ARRAY[]::TEXT[],ARRAY[]::JSONB[], $2)
        RETURNING log_id;
    """
    try:
      status = "connected" # need a red panda connection check fuction
      async with app.state.db.acquire() as connection:
          pipeline_id = await connection.fetchval(create_pipeline_query, pipeline.name, pipeline.connection, status)  
          print("pipeline_id", pipeline_id)
          await connection.execute(create_log_query, True, pipeline_id)     

          return JSONResponse(status_code=200, content={"message": "Pipeline created successfully"})
    except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error{e}")


@app.get("/logs/{pipeline_id}",
        #   dependencies=[Depends(JWTBearer())]
         )
async def get_logs(pipeline_id : str): 
    logs_query = f"SELECT * FROM logs WHERE pipeline_id = '{pipeline_id}'::uuid;" 
    async with app.state.db.acquire() as connection:
        row = await connection.fetchrow(logs_query)
        logs = dict(row) if row else None
        logs = {
        key: (
            [json.loads(log) for log in value] if key == 'logs' 
            else str(value) if isinstance(value, uuid.UUID) 
            else value
        ) 
        for key, value in dict(row).items()
    }
        
    print("logs",)
    pipeline_query = f"SELECT * FROM pipeline WHERE id = '{pipeline_id}'::uuid"
    async with app.state.db.acquire() as connection:
        pipeline_row = await connection.fetchrow(pipeline_query)
        pipeline = {key: (str(value) if isinstance(value, uuid.UUID) else value) for key, value in dict(pipeline_row).items()}

    return JSONResponse(status_code=200, content={"logs": logs, "pipeline": pipeline})


@app.post("/logs/create",
        #   dependencies=[Depends(JWTBearer())]
        )
async def create_logs(logs : LogRequestSchema = Body(...)):  
          
    if logs in [None , ""]:    
      raise HTTPException(status_code=404, detail=f"Error Log not founds")

    try :  
        fetch_logs_notify_teams = f"""
        SELECT notify_team FROM logs WHERE log_id = '{logs.log_id}'::uuid;
        """
        fetch_logs_teams = f"""
        SELECT team_members FROM logs WHERE log_id = '{logs.log_id}'::uuid;
        """
        async with app.state.db.acquire() as connection:
          notify_teams = await connection.fetchval(fetch_logs_notify_teams)     
          teams = await connection.fetchval(fetch_logs_teams)                   
        print(notify_teams, teams)
    except Exception as e :
        raise HTTPException(status_code=404, detail=f"Failed fetch pipeline: Error{e}")
    
    try :  
        fetch_pipeline_connection = f"""
        SELECT name FROM pipeline WHERE id = '{logs.pipeline_id}'::uuid;
        """
        async with app.state.db.acquire() as connection:
            connection_type = await connection.fetchval(fetch_pipeline_connection)        
            print("connection_type", connection_type)
    except Exception as e : 
        raise HTTPException(status_code=500, detail=f"Failed connection_type: Error{e}")
    

    try : 
        ai_response = await invoke_llm(logs.error_log, connection_type)
        # ai_response = re.sub(r'\bf', '', ai_response)
        print("ai_response", ai_response)
    except Exception as e :
        log = { 
            "a_id" : str(uuid.uuid4()),
            "error" : logs.error_log,
            "ai_response" : f"Failed LLM: Error{e}",
            "status" : "500",
            "action" : notify_teams,
        }
        
        append_log_query = f"""
        UPDATE logs
        SET logs = logs || '{json.dumps(log)}'::JSONB
        WHERE log_id = '{logs.log_id}'::uuid
        RETURNING log_id;
        """
        async with app.state.db.acquire() as connection:
          await connection.execute(append_log_query)   
        raise HTTPException(status_code=500, detail=f"Failed LLM: Error{e}")

    try : 
        if notify_teams: 
                await send_mail( 
                    email_lst = ['ndrohith09@gmail.com'], 
                    content = ai_response, 
                    )
                print("notified team")
    except Exception as e :
            print(f"Failed Mail Error: {e}")

    log = { 
        "a_id" : str(uuid.uuid4()),
        "error" : logs.error_log,
        "ai_response" : ai_response,
        "status" : "200",
        "action" : notify_teams,
    }
    
    append_log_query = f"""
    UPDATE logs
    SET logs = logs || '{json.dumps(log)}'::JSONB
    WHERE log_id = '{logs.log_id}'::uuid
    RETURNING log_id;
    """
    print("append_log_query", append_log_query)

    try: 
      async with app.state.db.acquire() as connection:
          await connection.execute(append_log_query)  
             
          return JSONResponse(status_code=200, content={"message": "Pipeline created successfully", "log" : log})
    except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error{e}")

        

@app.post("/logs/team",
        #   dependencies=[Depends(JWTBearer())]
          )
async def add_teams(teams : TeamSchema = Body(...)): 
    
    if teams.notify_team in [True, False, 'true', 'false']:
      try : 
          notify_team_query = f"""
          UPDATE logs SET notify_team = {teams.notify_team} WHERE log_id = '{teams.log_id}'::uuid;
          """
          async with app.state.db.acquire() as connection:
            await connection.execute(notify_team_query)        
      except Exception as e :
          raise HTTPException(status_code=404, detail=f"Failed Notify Team: Error{e}")
    print(teams.mail_id)
    if teams.mail_id not in [None, "", "null"]:      
        try :  
            team_members_query = f"""
            UPDATE logs
            SET team_members = team_members || '{teams.mail_id}'::TEXT
            WHERE log_id = '{teams.log_id}'::uuid
            RETURNING log_id;
            """
            async with app.state.db.acquire() as connection:
                await connection.execute(team_members_query)        
        except Exception as e :
            raise HTTPException(status_code=404, detail=f"Failed Team Members: Error{e}")
 
async def invoke_llm(error: str, errortype:str):    
  
  query = f'''
  {errortype} Error Log Format: [Time], [Level], Content 
  {error}
  '''

  inputs = [HumanMessage(content=query)]
  tool_llm_aimessage = llm_agent.invoke({"messages": inputs})
  res = draft_email_format(llm, tool_llm_aimessage['messages'][-2].content , errortype, error, tool_llm_aimessage['messages'][-1].content)
  print(res)
  return res.content
#   return JSONResponse(status_code=200, content={"message": res.content})
 
async def send_mail(email_lst, content):  
    # content = decode_byte(content) 

    # decoded_content = base64.b64decode(content).decode("utf-8")
          
    template = f'''
		<html>
		<body>
		

        <p>Hi !!!
        {content}
    		<br>Thanks for using panda.ai, keep using it..!!!</p> 

		</body>
		</html>
		''' 
    message = MessageSchema(
		subject="Fastapi-Mail module",
		recipients=email_lst, # List of recipients, as many as you can pass 
		body=template,
		subtype="html"
		)
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message) 
	
    return "email has been sent"



#  TODO : check func
''' ====================== User AUTH ======================'''

@app.post("/register", tags=["user"])
async def create_user(user: UserSchema = Body(...)):

    user_query = """
        SELECT * FROM users;
    """

    create_user_query = """
        INSERT INTO users (username, password) VALUES ($1, $2)"
    """
    try: 
      async with app.state.db.acquire() as connection:
            users = await connection.execute(user_query)  
            if any(x[1] == user.username for x in users):
                    raise HTTPException(status_code=400, detail='Username already exists') 
            hashed_password = get_password_hash(user.password)  
            
            await connection.execute(create_user_query, user.username, hashed_password)   
            sign = signJWT(user.username)
            return JSONResponse(status_code=200, content={"message": sign})
    except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error{e}")


@app.post("/login", tags=["user"])
async def user_login(auth_details: UserLoginSchema = Body(...)):
     
    user = None
    user_query = """
        SELECT * FROM users;
    """

    try: 
        async with app.state.db.acquire() as connection:
            users = await connection.execute(user_query)  
            for x in users:
                print(x[1] , x[2], auth_details.username)
                if x[1] == auth_details.username:
                    user = x 
                    break
            if (user is None) or (not verify_password(auth_details.password, user[2])):
                raise HTTPException(status_code=401, detail='Invalid username and/or password')
            
            sign =  signJWT(user[1])
            return JSONResponse(status_code=200, content={"message": sign})
    except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error{e}")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)