from pydantic import BaseModel,EmailStr
from typing import Optional,List,Dict

from datetime import datetime,date


class GetUser(BaseModel):
    email: EmailStr
    username: Optional[str]
    
    class Config:
        orm_mode = True
        
        
class LoginUser(BaseModel):
    email: EmailStr
    hashed_password: str
    
    class Config:
        orm_mode = True
        
        
class PostUser(BaseModel):
    email: EmailStr
    username: str
    hashed_password:str
    
    class Config:
        orm_mode= True
        