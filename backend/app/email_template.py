from langchain_core.prompts import PromptTemplate

def draft_email_format( llm : any, input : str, errortype:str, error:str, solution:str):
    system = """
    You are tasked with formatting the content strictly in the following format without adding extra information or explanation: 
    Extract EventId, EventTemplate, Level from the {input} and format accordingly.
    """


    e_prompt_template = PromptTemplate(
    input_variables=["input"], 
    template = system) 

    e_prompt = e_prompt_template.format(input = input)
    event = llm.invoke(e_prompt) 

    system_template = """
    You are tasked with formatting the content strictly in the following format without adding extra information or explanation:

    {errortype} Error

    {event}

    Error: {error}
    {solution}
    """

    prompt_template = PromptTemplate(
    input_variables=["event", "error", "solution"], 
    template = system_template) 


    prompt = prompt_template.format(event = event.content, errortype = errortype, error = error, solution = solution)
    result = llm.invoke(prompt) 
    return result
