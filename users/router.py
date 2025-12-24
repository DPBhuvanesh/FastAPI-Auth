from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from core.database import get_db
from users.schema import PostUser
from users.services import create_user_account
from fastapi.responses import JSONResponse
from auth.services import get_current_active_user
from users.schema import GetUser
from users.models import User
from auth.services import get_current_user 

router = APIRouter(
    prefix='/users',
    tags=['User']
)

@router.get("/profile")
async def user_profile():
    return {"message": "User Profile"}

@router.post('',status_code=status.HTTP_201_CREATED)
async def create_user(data: PostUser, db:Session= Depends(get_db)):
   await create_user_account(data=data,db=db)
   payload = {"message":"User account has been created"}
   return JSONResponse(content=payload)


@router.get('/me',response_model=GetUser)
async def user_list(current_user:User = Depends(get_current_active_user)):
    return current_user


@router.get("/test-token")
async def test_token(current_user: User = Depends(get_current_user)):
    return {"user": current_user.email}