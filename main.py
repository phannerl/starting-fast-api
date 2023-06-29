from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "email": "john@gmail.com",
        "age":  18
    }
}

class Student(BaseModel):
    name: str
    email: str
    age: int

class UpdateStudent(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]

@app.get("/")
def root():
    return {"message": "Hello, world"}

# GET /get-student -> get all students
@app.get("/get-student")
def get_student():
    return students

# GET /get_by_id/123 -> get student information by student ID
@app.get("/get-by-id/{students_id}")
def get_by_id(students_id: int = Path(description="Student ID of the student You are looking for", gt=0, lt=3)):
    return students[students_id]

# GET /get-by-name -> get student information by name
@app.get("/get-by-name")
def get_by_name(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"].lower() == name.lower():
            return students[student_id]
    return {"student": "No data"}


# POST /create_new_student
@app.post("/create_new_student")
def create_new_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": {"Student Exists"}}
    
    students[student_id] = student
    return {"student": students[student_id]}

# PUT /create_new_student
@app.put("/update_student")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name is not None:
        students[student_id].name = student.name
    if student.email is not None:
        students[student_id].email = student.email
    if student.age is not None:
        students[student_id].age = student.age
    return {"student": students[student_id]}

# DELETE /delete_student
@app.delete("/delete_student")
def update_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    del students[student_id]
    
    return {"students": students}
