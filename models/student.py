from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str
    email: str


class Student(StudentCreate):
    id: Optional[str] = Field(alias="_id")


    class Config:
        populate_by_name = True