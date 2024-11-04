from devices.core.database import get_session
from fastapi import Header, HTTPException, status
from devices.token.services import verify_token
from devices.token.schemas import TokenData


def get_db():
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Header(...)) -> TokenData:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return verify_token(token)
