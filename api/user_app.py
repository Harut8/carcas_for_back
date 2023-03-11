from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.UserModel import TokenSchema
from auth.jwt_logic import verify_password, create_access_token, create_refresh_token
from api.ApiRoutes import ApiRoutes
from services.MainService import MainService

user_app = APIRouter(tags=['USER LOGIC'])


@user_app.post(
    ApiRoutes.login,
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MainService.check_email_and_password(
        email=form_data.username,
        password=form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }