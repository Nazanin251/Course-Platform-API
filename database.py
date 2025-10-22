
from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017")
db=client["course_selling"]
instructor_col=db["instructors"]
courses_col=db["courses"]
students_col=db["students"]
enrollments_col=db["enrollments"]
