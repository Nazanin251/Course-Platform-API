from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EnrollmentCreate(BaseModel):
    student_id:str
    course_id:str

class Enrollment(EnrollmentCreate):
    id: Optional[str] = Field(alias="_id")
    timestamp: Optional[datetime] = None

    class Config:
        populate_by_name = True