from typing import List

from fastapi import FastAPI, HTTPException, APIRouter,status

from models.instructors import Instructor, InstructorCreate
from database import *
from bson import ObjectId



instructor_router = APIRouter(prefix="/instructors", tags=["instructors"])


@instructor_router.post("/", response_model=Instructor,status_code=status.HTTP_201_CREATED)
def create_new_instructor(new_instructor: InstructorCreate):
    res=instructor_col.insert_one(new_instructor.dict())
    return Instructor(id=str(res.inserted_id),**new_instructor.dict())

@instructor_router.get("/{instructor_id}", response_model=Instructor)
def get_instructor_by_id(instructor_id:str):
    instructor=instructor_col.find_one({"_id":ObjectId(instructor_id)})
    if not instructor:
        raise HTTPException(status_code=404,detail="Instructor not found")
    instructor["_id"]=str(instructor["_id"])
    return instructor

@instructor_router.put("/{instructor_id}", response_model=Instructor)
def update_instructor(instructor_id:str, new_instructor: InstructorCreate):
    result=instructor_col.update_one({"_id":ObjectId(instructor_id)},{"$set":new_instructor.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404,detail="Instructor not found")
    updated_instructor=instructor_col.find_one({"_id":ObjectId(instructor_id)})
    updated_instructor["_id"]=str(updated_instructor["_id"])
    return updated_instructor

@instructor_router.delete("/{instructor_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(instructor_id:str):
    result=instructor_col.delete_one({"_id":ObjectId(instructor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Instructor not found")

@instructor_router.get("/", response_model=List[Instructor])
def list_instructors():
    instructors = list(instructor_col.find())
    for i in instructors:
        i["_id"] = str(i["_id"])
    return instructors