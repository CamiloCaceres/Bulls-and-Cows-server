from fastapi import FastAPI, Depends, status, HTTPException
from app.auth.models import User as UserModel
from app.auth.schemas import User as Userschema, UserCreate
from ..db import get_db

app = FastAPI()