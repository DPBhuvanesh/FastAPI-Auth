from users.models import User
from fastapi.exceptions import HTTPException
from core.security import secure_pwd
from pydantic import EmailStr
from sqlalchemy.orm import Session

async def create_user_account(data,db):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail='Email is already registered with us')
    
    name = db.query(User).filter(User.username == data.username).first()
    
    if name:
        raise HTTPException(status_code=422,detail = 'username is already registered with us')
    
    new_user = User(
        username = data.username,
        email = data.email,
        hashed_password=secure_pwd(data.hashed_password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db):
    return db.query(User).all()
def get_user(user_name: str,db):
    return db.query(User).filter(User.name == user_name).first()

def get_user_by_email(db : Session,user_email: EmailStr):
    return db.query(User).filter(User.email == user_email).first()

