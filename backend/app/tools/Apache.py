from pydantic import BaseModel, Field 
from langchain_core.tools import StructuredTool
from .embeddings import retrieve_apache_embeddings

class DebugApacheErrorLog(BaseModel):
    """Request schema for Debug Apache Error Log"""

    Level: str = Field( 
        ...,
        alias="Level",
        description="Provides severity level about the error log",        
    ) 

    Content: str = Field( 
        ...,
        alias="Content",
        description="Shows the error message of the event", 
    )
    

def debug_apache_error_log(Level:str,  Content:str):
        """ Read a debug Apache Error Log and return 
        Tool that retrieves solution from the existing logs if found, else creates a new solution
        
        Args:
            Level: Provides severity level about the error log 
            Content: Shows the error message of the event
        """
    
        print("log found", Content , Level)
        if  Content:
            output = retrieve_apache_embeddings(Level, Content)
            return output
        else:
            raise "Unknown Error"

debug_apache_error_log = StructuredTool.from_function(
    func=debug_apache_error_log,
    name="Debug Apache Error",
    description="Read a debug Apache Error Log and return",
    args_schema=DebugApacheErrorLog,  
) 