from pydantic import BaseModel


class AddRequestRefCode(BaseModel):
    code: str
    expire: int


class RefCode(AddRequestRefCode):
    user_id: int
