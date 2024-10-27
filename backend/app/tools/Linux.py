from pydantic import BaseModel, Field 
from langchain_core.tools import StructuredTool
from .embeddings import retrieve_linux_embeddings

class DebugLinuxErrorLog(BaseModel):
    """Request schema for Debug ZooKeeper Error Log"""

    Level: str = Field( 
        ...,
        alias="Level",
        description="Provides severity level about the error log",        
    ) 

    Component: str = Field( 
        ...,
        alias="Component",
        description="Shows the which component throws the error", 
    )

    Content: str = Field( 
        ...,
        alias="Content",
        description="Shows the error message of the event", 
    )
    

def debug_linux_error_log(Level:str, Component:str,  Content:str):
        """ Read a debug Linux Error Log and return 
        Tool that retrieves solution from the existing logs if found, else creates a new solution
        
        Args:
            Level: Provides severity level about the error log 
            Component: Shows the which component throws the error
            Content: Shows the error message of the event
        """
    
        print("log found", Content , Level)
        if  Content:
            output = retrieve_linux_embeddings(Level,Component, Content)
            return output
        else:
            raise "Unknown Error"

debug_linux_error_log = StructuredTool.from_function(
    func=debug_linux_error_log,
    name="Debug Linux Error",
    description="Read a debug Linux Error Log and return",
    args_schema=DebugLinuxErrorLog, 
) 
