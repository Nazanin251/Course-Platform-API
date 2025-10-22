from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    title: str
    instructor_id: str

class Course(CourseCreate):
    id: Optional[str] = Field(alias="_id")

    class Config:
        populate_by_name = True