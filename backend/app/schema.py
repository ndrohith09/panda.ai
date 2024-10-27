from pydantic import BaseModel, Field, EmailStr
from typing import List, Any,Optional

class PostSchema(BaseModel):
    name: str = Field(...)
    connection: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Linux",
                "connection": "connection string uri"
            }
        }

class TeamSchema(BaseModel):
    log_id: str = Field(...)
    notify_team: Optional[bool] = Field(...)
    mail_id: Optional[str] = Field(...)
    

class LogRequestSchema(BaseModel):
    pipeline_id: str = Field(...)
    log_id: str = Field(...)
    error_log: str = Field(...)
    
class LogResponseSchema(BaseModel):
    error_log: str = Field(...)
    ai_response: str = Field(...) 
    status: str = Field(...) 

    

class EmailSchema(BaseModel):
   email: List[EmailStr]
   content : Any 

class LLMSchema(BaseModel):
    error : str # Sample bytes: SnVuIDE2IDA0OjE2OjE3IGNvbWJvIHN1KHBhbV91bml4KVsyNTU0OF06IHNlc3Npb24gb3BlbmVkIGZvciB1c2VyIG5ld3MgYnkgKHVpZD0wKQ
    errortype : str


class UserSchema(BaseModel):
    username: str = Field(...) 
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Joe Doe", 
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "joe@xyz.com",
                "password": "any"
            }
        }