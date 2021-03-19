from app.config import JWT_SECRET
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.hash import bcrypt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_pwd(password, hashed_password):
    return bcrypt.verify(password,hashed_password)


