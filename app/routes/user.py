from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from google.cloud.firestore_v1.base_query import FieldFilter
from auth.jwt import create_access_token, get_current_user
from schemas.user import User
from service import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_router = APIRouter(tags=["Users"])


@user_router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users = (
        db.collection("users")
        .where(filter=FieldFilter("email", "==", form_data.username))
        .get()
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not users:
        raise credentials_exception
    user = users[0].to_dict()
    if not pwd_context.verify(form_data.password, user["password"]):
        raise credentials_exception
    access_token = create_access_token(
        {"sub": user.get("email"), "admin": user.get("admin")}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/register")
async def register(payload_data: User):
    users_collection = db.collection("users")
    users = users_collection.where(
        filter=FieldFilter("email", "==", payload_data.email)
    ).get()
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    payload_data.password = pwd_context.hash(payload_data.password)
    _, doc = users_collection.add(payload_data.to_dict())
    return {"message": f"User created successfully with ID {doc.id}"}


@user_router.get("/users/")
async def read_user_by_email(user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user account"
        )
    return user
