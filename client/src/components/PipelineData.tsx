import { Button, Form, Input, Modal, Switch, Table, TableColumnsType, Tag, Tooltip } from "antd";
import Navbar from "./Navbar";
import { ArrowsUpDownIcon, CalendarDaysIcon, ClockIcon, PlusIcon } from "@heroicons/react/24/outline";
import { useEffect, useState } from "react";
import FormItem from "antd/es/form/FormItem";
import { useParams } from "react-router-dom";
import instance from "axios-instance";

interface Log {
  log_id: string
  notify_team: boolean,
  team_members: string[],
  logs: CurrentLog[],
}

type FormValue = {
  mail_id :string,
}
interface CurrentLog {
    a_id: string
    error: string,
    status: string,
    ai_response: string,
    action: boolean,
}

const PipelineData = () => {

  const [pipeline, setPipeline] = useState<any>({});
  const [log, setLog] = useState<Log>();
  const [currentLog, setCurrentLog] = useState<CurrentLog>();
  const [isActionOpen, setIsActionOpen] = useState(false);
  const { id }  = useParams();  


  useEffect(() => { 

    try {
      instance({
        url: `logs/${id}`,
        method: "GET",
      })
      .then((res) => {
        // handle success
        setPipeline(res.data.pipeline);
        setLog(res.data.logs);
        setCurrentLog(res.data.logs.logs[0])
        console.log(res);              
      });
    } catch (e) {
      // handle error
      console.error(e);   
    }  

  },[id])

    const content = `EventId: E50 
EventTemplate: Unexpected Exception:
Level: [Level]  

Error: Jun 16 04:16:17 combo su(pam_unix)[25548]: session opened for user news by (uid=0)

Solution: The error log indicates a session opened for user news by (uid=0). This might be an indication of unauthorized access or an unexpected system behavior. It is recommended to investigate further and ensure that the user's session is legitimate and properly authenticated. Additionally, reviewing the system logs and authentication records can help identify any potential security vulnerabilities.
`

const notifyTeam =  async ( ) => {
  var data = {
    mail_id: null,
    log_id : log?.log_id,
    notify_team : !log?.notify_team
  };
  try {
    await instance({ 
      url: "logs/team",
      method: "POST",
      data: data,
    }).then((res) => { 
      console.log(res); 
      window.location.reload();
    });
  } catch (e) {
    // handle error
    console.error(e);
  }
}

const addTeam =  async (form: FormValue ) => {
  var data = {
    mail_id: form.mail_id,
    log_id : log?.log_id,
    notify_team : null
  };
  try {
    await instance({ 
      url: "logs/team",
      method: "POST",
      data: data,
    }).then((res) => { 
      console.log(res); 
      window.location.reload();
    });
  } catch (e) {
    // handle error
    console.error(e);
  }
}

function randomInt(min : any, max : any) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

  return (
    <>
      <main className="ml-64 flex-1 bg-white dark:bg-dark-bgColor">
        <Navbar title={`Pipeline / ${pipeline.name}`} />
        <div className="relative pt-20 px-10 w-full flex h-screen flex-col p-4">
            <div className="flex px-6 items-center space-x-5">
          <Button className="w-auto" 
        onClick={() => setIsActionOpen(true)}          
        color="default" variant="outlined">
            Configurations
          </Button>   
          <Button className="w-auto" 
        onClick={() => setIsActionOpen(true)}          
        color="default" variant="outlined">
            Team
          </Button>
          <Tooltip title="Notify teams" >
          <Switch className="w-10" checked={log?.notify_team} onChange={notifyTeam} />
            </Tooltip>          
          {pipeline.status ==="connected" ? <Tag color="green">Pipeline Running</Tag> : <Tag color="red">Pipeline InActive</Tag> }
              </div>

          <div className="w-full bg-white pt-4">
      <div className="mx-5"> 
         
        <div
          className={`grid grid-cols-12 border-2 border-slate-100`}
          style={{ height: "calc(100vh - 10rem)" }}
        >
          <div className="col-span-3 overflow-scroll border-r-2 border-slate-100">
            <h4 className="my-2 ml-2 inline-flex font-semibold text-gray-600">
            
      Pipeline Logs <p className="text-red">&nbsp;({log?.logs.length})</p>
      </h4> 

              <table className="w-full text-left text-sm text-gray-500">
                <tbody> 

                  {log && log.logs.length > 0  ? log?.logs.map((log, idx) => (
                      <tr key={idx}> 
                      <td
                      onClick = {
                        () =>  { 
                          setCurrentLog(log); 
                        }
                      }
                        className={`mx-1 flex cursor-pointer items-center space-x-2 py-2 hover:rounded hover:bg-bgColor ${currentLog?.a_id === log.a_id && 'bg-bgColor'}`}
                      >
                         
                        <Tag color={log.status > "400" ? 'red' : 'green'}>{log.status}</Tag>            


                        <p className="text-xs">{log.error}</p>
                      </td>
                    </tr> 
                  )) : (
                    <>No logs found</>
                  )}
                      
                
                </tbody>
              </table>
            </div> 
            {currentLog ? (
          <div className="col-span-8 overflow-scroll px-4">
            
              <h4 className="mr-2 mt-4 font-semibold text-gray-600">Error Log</h4>
            <div className="my-2 flex items-center space-x-2 text-gray-500">


              <Tag color="blue">{currentLog?.error}</Tag>            
              <Tag color={currentLog && currentLog?.status > "400" ? 'red' : 'green'}>{currentLog?.status}</Tag>            
              {currentLog?.action ? <Tag color="green">Notified Team</Tag> : <Tag color="red">Action Not Taken</Tag>} 

              <div className="flex items-center space-x-1 text-xs font-bold">
                <ClockIcon className="text-secondary w-4 h-4" /> <p>{randomInt(20, 60)} ms</p>
              </div>

              <div className="flex items-center space-x-1 text-xs font-bold">
                <ArrowsUpDownIcon className="text-secondary w-4 h-4" /> <p>{randomInt(20, 60)} kb</p>
              </div>

              <div className="flex items-center space-x-1 text-xs font-bold">
                {/* <CalendarDaysIcon className="text-secondary w-4 h-4" /> <p>20th July, 2024</p> */}
                {/* <CalendarDaysIcon className="text-primary" /> <p>{convertTimeStampToDateTime(currentLog.created_at)}</p> */}
              </div>             
            </div>
            <div>
                
            </div>
 
            <h4 className="mr-2 mt-4 font-semibold text-gray-600">AI Response</h4>
            <div className="m-2 h-auto max-h-4xl text-sm rounded-sm border overflow-auto">
              <p className="px-4 py-2 flex justify-start whitespace-pre-wrap text-tertiary prose-sm">{currentLog?.ai_response}</p>
            </div>
  
          </div>
          ) : (
            <p></p>
          )}
        </div> 
      </div>
    </div>

    
    
        </div>
      </main> 


      <Modal
        style={{ top: "5rem" }}
        open={isActionOpen}
        footer={false}
        onCancel={() => setIsActionOpen(false)}
      >
        <h1 className="text-xl font-medium dark:text-dark-textColor">
          My Team
        </h1>
        <br />

        {log?.team_members.map((member , idx) => (
          <Tag 
          closable={true}
          >{member}</Tag>
        ))}

<br />
<br />
        <div className={"min-h-auto max-h-[36rem] space-y-6 overflow-y-auto"}>
        <Form onFinish={addTeam}>
        <Form.Item<FormValue>
        label="Mail ID"
        name="mail_id"
        rules={[{ required: true, message: 'Please input your mail id!' }]}
        >
        <Input type="email" />
        </Form.Item>
 
      <Button color="default"  variant="filled" htmlType="submit">
        Add
      </Button> 

        </Form>
        </div>
      </Modal>

    </>
  );
};
export default PipelineData;
