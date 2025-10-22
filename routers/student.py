from fastapi import  HTTPException, APIRouter,status
from typing import List
from models.student import Student, StudentCreate
from database import *
from bson import ObjectId

student_router = APIRouter(prefix="/students", tags=["students"])

@student_router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(new_student: StudentCreate):
    res = students_col.insert_one(new_student.dict())
    return Student(id=str(res.inserted_id), **new_student.dict())


@student_router.get("/{student_id}", response_model=Student)
def get_student(student_id:str):
    student=students_col.find_one({"_id":ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404,detail="Student not found")
    student["_id"] = str(student["_id"])
    return student

@student_router.put("/{student_id}", response_model=Student)
def update_student(student_id: str, new_student: StudentCreate):
    result = students_col.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": new_student.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = students_col.find_one({"_id": ObjectId(student_id)})
    updated_student["_id"] = str(updated_student["_id"])
    return updated_student

@student_router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str):
    result = students_col.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

@student_router.get("/", response_model=List[Student])
def list_students():
    students = list(students_col.find())
    for student in students:
        student["_id"] = str(student["_id"])
    return students
