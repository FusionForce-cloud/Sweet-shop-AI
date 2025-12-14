from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetOut(SweetCreate):
    id: int

class SweetUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    quantity: int | None = None