from fastapi import FastAPI, HTTPException, APIRouter,status
from typing import List
from database import *
from models.course import Course , CourseCreate
from bson import ObjectId

course_router =APIRouter(prefix="/courses", tags=["courses"])

@course_router.post("/", response_model=Course,status_code=status.HTTP_201_CREATED)
def create_course(new_course: CourseCreate):
    res=courses_col.insert_one(new_course.dict())
    return Course(id=str(res.inserted_id),**new_course.dict())

@course_router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id:str):
    course=courses_col.find_one({"_id":ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    course["_id"]=str(course["_id"])
    return  course

@course_router.put("/{course_id}", response_model=Course)
def update_course(course_id:str, new_course: CourseCreate):
    result=courses_col.update_one({"id":ObjectId(course_id)},{"$set":new_course.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404,detail="Course not found")
    updated_course=courses_col.find_one({"id":ObjectId(course_id)})
    updated_course["_id"]=str(updated_course["_id"])
    return updated_course

@course_router.delete("/{course_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id:str):
    result=courses_col.delete_one({"_id":ObjectId(course_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Course not found")


@course_router.get("/", response_model=List[Course])
def list_courses():
    courses = list(courses_col.find())
    for course in courses:
        course["_id"] = str(course["_id"])
        if "instructor_id" in course and isinstance(course["instructor_id"], ObjectId):
            course["instructor_id"] = str(course["instructor_id"])
    return courses

@course_router.get("/instructor/{instructor_id}", response_model=List[Course])
def get_courses_by_instructor(instructor_id: str):

    courses = list(courses_col.find({"instructor_id": ObjectId(instructor_id)}))
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for this instructor")

    for c in courses:
        c["_id"] = str(c["_id"])
    return courses
