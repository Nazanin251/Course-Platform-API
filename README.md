# 🎓 Course Platform API (FastAPI + MongoDB)

#### A simple RESTful API built with FastAPI and MongoDB, designed to manage students, instructors, courses and enrollments.
#### This project demonstrates full CRUD functionality and clean API routing using FastAPI


## 🚀 Features
- Create, read, update, and delete (CRUD) operations for:
    - Instructors 👩‍🏫
    - Students 👨‍🎓
    - Courses 📚
    - Enrollments 📝

- Organized with separate `routers`, `models`, and `database` modules
- MongoDB connection via `pymongo`


## ⚙️ Installation & Run

1. Create & activate virtual environment
```bash
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```
---
2. Install dependencies
```bash 
pip install fastapi "uvicorn[standard]" pymongo
```
---
3. Run the server
```bash 
uvicorn main:app --reload
```
---


## 📁 Project Structure
```bash
📦 Course Platform
 ┣ 📂 models
 ┣ 📂 routers
 ┣ 📜 database.py
 ┣ 📜 main.py
 ┗ 📜 README.md
```
---


## 🧩 Tech Stack
- Backend: FastAPI
- Database: MongoDB
- ODM/Driver: PyMongo
- Server: Uvicorn