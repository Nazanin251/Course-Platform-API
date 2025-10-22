from models.enrollment import Enrollment, EnrollmentCreate
from database import *
from bson import ObjectId
from fastapi import HTTPException, APIRouter, status
from typing import List, Dict, Any
from datetime import datetime

enrollment_router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@enrollment_router.get("/", response_model=List[Enrollment])
def list_enrollments():
    enrollments = list(enrollments_col.find())
    for e in enrollments:
        e["_id"] = str(e["_id"])
        e["student_id"] = str(e["student_id"])
        e["course_id"] = str(e["course_id"])
    return enrollments


@enrollment_router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate):

    if enrollments_col.find_one({
        "student_id": ObjectId(payload.student_id),
        "course_id": ObjectId(payload.course_id)
    }):
        raise HTTPException(status_code=409, detail="Already enrolled")

    doc = {
        "student_id": ObjectId(payload.student_id),
        "course_id": ObjectId(payload.course_id),
        "timestamp": datetime.utcnow(),
    }
    res = enrollments_col.insert_one(doc)

    return {
        "_id": str(res.inserted_id),
        "student_id": payload.student_id,
        "course_id": payload.course_id,
        "timestamp": doc["timestamp"]
    }


@enrollment_router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: str):
    res = enrollments_col.delete_one({"_id": ObjectId(enrollment_id)})
    if res.deleted_count != 1:
        raise HTTPException(status_code=404, detail="Enrollment not found")


@enrollment_router.get("/students/{student_id}/courses/", response_model=List[Dict[str, Any]])
def get_courses_for_student(student_id: str):
    enrolls = list(enrollments_col.find({"student_id": ObjectId(student_id)}))
    course_ids = [ObjectId(e["course_id"]) for e in enrolls]

    if not course_ids:
        return []

    courses = list(courses_col.find({"_id": {"$in": course_ids}}))
    for c in courses:
        c["_id"] = str(c["_id"])
        if "instructor_id" in c and isinstance(c["instructor_id"], ObjectId):
            c["instructor_id"] = str(c["instructor_id"])
    return courses


@enrollment_router.get("/courses/{course_id}/students/", response_model=List[Dict[str, Any]])
def get_students_for_course(course_id: str):
    enrolls = list(enrollments_col.find({"course_id": ObjectId(course_id)}))
    student_ids = [ObjectId(e["student_id"]) for e in enrolls]
    if not student_ids:
        return []

    students = list(students_col.find({"_id": {"$in": student_ids}}))
    for s in students:
        s["_id"] = str(s["_id"])
    return students