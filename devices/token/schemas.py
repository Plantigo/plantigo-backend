from uuid import UUID

from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: UUID
