from pydantic import BaseModel

from app.enums.user_type import UserType
from app.models.user_data import UserData


class Registro(UserData):
    password: str


class LoginReturn(BaseModel):
    user_type: UserType
    access_token: str
    token_type: str


class ExistsEmail(BaseModel):
    exists: bool
