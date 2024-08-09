from  fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import User as UserModel
from app.auth.schemas import User as UserSchema, UserCreate
from app.db import get_db
import app.auth.service as auth_service



app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"hello world"}

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await auth_service.existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username or email already in use")
    db_user = await auth_service.create_user(db, user)
    access_token = await auth_service.create_access_token(db_user.id, db_user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username
    }


@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = await auth_service.authenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    access_token = await auth_service.create_access_token(db_user.id, db_user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        }





# https://www.youtube.com/watch?v=Mpcn2CZZW34 min 27