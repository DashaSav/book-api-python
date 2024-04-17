from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from src.db import get_book_collection


router = APIRouter(prefix="/books", tags=["books"])

