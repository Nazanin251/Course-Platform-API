from fastapi import FastAPI

from routers.enrollment import enrollment_router
from routers.student import student_router
from routers.course import course_router
from routers.instructor import instructor_router

app = FastAPI(title="Course Platform")
app.include_router(enrollment_router)
app.include_router(student_router)
app.include_router(course_router)
app.include_router(instructor_router)