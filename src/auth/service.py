from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt

from models import User as UserModel
from schemas import User as UserSchema, UserCreate

SECRET_KEY = "mysecretkey"
EXPIRE_MINUTES = 60 * 24

# check existing user with same username or email
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None

# create token
# jwt = {encoded data, secret key, algorithm}
async def create_access_token(id: int, username: str):
    encode = {"sub": username, "id": id}
    expires = datetime.now(datetime.UTC) + timedelta(minutes=EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm="HS256")