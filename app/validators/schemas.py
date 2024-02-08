from typing import List

from pydantic import BaseModel,EmailStr


class UsersCreate(BaseModel):
    type: str
    full_name: str
    username : str
    email: EmailStr
    password: str
    submitted_by = str

class CoursesCreate(BaseModel):
    course_name: str
    semester: str
    class_: str
    lecture_hour : str
    submitted_by = str

class StudentsCreate(BaseModel):
    full_name: str
    semester: str
    class_: str
    submitted_by = str

class DepartmentCreate(BaseModel):
    department_name: str
    submitted_by = str

class Attendance_logCreate(BaseModel):
    present: bool
    submitted_by = str


class User(UsersCreate):
    id: int

    class Config:
        orm_mode = True

class Students(StudentsCreate):
    id: int

    class Config:
        orm_mode = True


class Courses(CoursesCreate):
    id: int

    class Config:
        orm_mode = True


class Department(DepartmentCreate):
    id: int

    class Config:
        orm_mode = True


class Attendance_log(Attendance_logCreate):
    id: int

    class Config:
        orm_mode = True
