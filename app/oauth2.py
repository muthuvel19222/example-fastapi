from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire

def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})
    print(to_encode)
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    
    return encoded_jwt
    
def verify_access_token(token:str, credential_execption):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str=payload.get("user_id") # type: ignore
        if  id is None:
           raise credential_execption
        token_data=schema.TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_execption
    
def get_current_user(token: str=Depends(Oauth2_scheme)):
    credential_execption=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate':'Bearer'})

    return verify_access_token(token, credential_execption)