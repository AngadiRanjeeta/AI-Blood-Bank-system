from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db

router = APIRouter()

@router.get("/")
def home():
    return {"message": "AI Blood Bank System Running"}