from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Sweet
from ..schemas import SweetCreate, SweetOut, SweetUpdate
from ..auth import get_current_user, get_current_admin

router = APIRouter(prefix="/api/sweets")

router = APIRouter(prefix="/api/sweets")

@router.post("/", response_model=SweetOut)
def add_sweet(sweet: SweetCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    s = Sweet(**sweet.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.get("/", response_model=list[SweetOut])
def list_sweets(db: Session = Depends(get_db)):
    return db.query(Sweet).all()

@router.get("/search", response_model=list[SweetOut])
def search_sweets(
    name: str = Query(None),
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Sweet)
    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)
    return query.all()

@router.put("/{id}", response_model=SweetOut)
def update_sweet(id: int, sweet: SweetUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    s = db.get(Sweet, id)
    if not s:
        raise HTTPException(404, "Sweet not found")
    for key, value in sweet.model_dump(exclude_unset=True).items():
        setattr(s, key, value)
    db.commit()
    db.refresh(s)
    return s

@router.delete("/{id}")
def delete_sweet(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    s = db.get(Sweet, id)
    if not s:
        raise HTTPException(404, "Sweet not found")
    db.delete(s)
    db.commit()
    return {"msg": "Sweet deleted"}

@router.post("/{id}/purchase", response_model=SweetOut)
def purchase(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    sweet = db.get(Sweet, id)
    if not sweet:
        raise HTTPException(404, "Sweet not found")
    if sweet.quantity <= 0:
        raise HTTPException(400, "Out of stock")
    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)
    return sweet

@router.post("/{id}/restock", response_model=SweetOut)
def restock(id: int, quantity: int = Query(..., gt=0), db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    sweet = db.get(Sweet, id)
    if not sweet:
        raise HTTPException(404, "Sweet not found")
    sweet.quantity += quantity
    db.commit()
    db.refresh(sweet)
    return sweet
