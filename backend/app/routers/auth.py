from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import User
from ..schemas import UserCreate, Token
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth")

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(400, "Username already registered")
    is_admin = user.username == "admin"
    db_user = User(username=user.username, password=hash_password(user.password), is_admin=is_admin)
    db.add(db_user)
    db.commit()
    return {"msg": "User registered"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
