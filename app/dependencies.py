from typing import Annotated
from fastapi import Depends

from app.database.local import Database

db = Database()

def get_database() -> Database:
    return db

