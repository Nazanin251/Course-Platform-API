
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class InstructorCreate (BaseModel):
    name:str

class Instructor (InstructorCreate):
    id: Optional[str] = Field(alias="_id")
    class Config:
        populate_by_name = True



