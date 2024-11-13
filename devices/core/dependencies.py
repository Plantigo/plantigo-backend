from typing import Optional

from core.database import get_session
from fastapi import Header, HTTPException, status
from auth_token.schemas import TokenData
from plantigo_common.auth.token_service import verify_token
from core.settings import settings


def get_db():
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: Optional[str] = Header(None)) -> TokenData:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = verify_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
    return TokenData(user_id=payload.get('user_id'))
