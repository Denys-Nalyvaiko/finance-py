from fastapi import APIRouter, HTTPException, Request
from starlette import status
from app.models.models import User
from app.dependencies import db_dependency
from app.schemas import auth_schema


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(register_user_request: auth_schema.RegisterUserRequest, db: db_dependency):
    user = User(
        email=register_user_request.email,
        password=register_user_request.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"email": user.email, "password": user.password}