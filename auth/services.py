import jwt.exceptions
from core.config import setting
from core.security import oauth2_scheme 
from core.database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone
from users.services import get_user_by_email
from core.security import verify_pwd
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from auth.schema import TokenData
from users.models import User

def authenticate_user(email:str,password:str,db:Session = Depends(get_db)):
    
    user= get_user_by_email(db,email)
    if not user:
        return False
    if not verify_pwd(password,user.hashed_password):
        return False
    return user


def create_access_token(data:dict,expire_delta:timedelta | None=None):
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
        
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,setting.secret_key,algorithm =setting.algorithm)
    
    return encoded_jwt

def get_current_user(token : Annotated[str, Depends(oauth2_scheme)],db:Session =Depends(get_db)):
        credential_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'},
        )
        
        try:
            payload = jwt.decode(token,setting.secret_key,algorithms = [setting.algorithm])
            email = payload.get('sub')
            if email is None:
                raise credential_exception
            token_data = TokenData(email=email)
            
        except InvalidTokenError:
            raise credential_exception
        
        user = get_user_by_email(db,token_data.email)
        if user is None:
            raise credential_exception
        return user
    
def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user