from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from google.cloud.firestore_v1.base_query import FieldFilter

from service import db
from config import config

SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    def credentials_exception(detail: str):
        return HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload is None:
        raise credentials_exception("Could not validate credentials")
    expire = payload.get("exp")
    if expire < int(datetime.now().strftime("%s")):
        raise credentials_exception("Credentials are expired")
    return payload.get("sub")


def get_current_user(email: str = Depends(get_user)):
    users = db.collection("users").where(filter=FieldFilter("email", "==", email)).get()
    if users:
        user = users[0]
        return {"id": user.id, **user.to_dict()}
    return None
