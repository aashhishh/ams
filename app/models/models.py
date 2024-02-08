from sqlalchemy import Column, ForeignKey, Integer, String, Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

from app.services.db import Base

def current_time():
    localized_time = datetime.now()
    naive_time = localized_time.replace(tzinfo=None)
    return naive_time

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True,index=True)
    type= Column(String, nullable=False)
    full_name = Column(String,nullable=False,)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    password = Column(String,nullable=False,)
    submitted_by = Column(String,nullable=False,) 
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)
    
class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True,index=True)
    course_name= Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.id"),nullable=False)
    semester = Column(String, nullable=False)
    class_ = Column(String, nullable=False)
    lecture_hour = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True,index=True)
    full_name = Column(String,unique=True, nullable=False)
    department_id = Column(String, ForeignKey("departments.id"),nullable=False)
    semester = Column(String, nullable=False)
    class_ = Column(String, nullable=False,index=True)
    submitted_by = Column(String())
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True,index=True)
    department_name= Column(String,unique = True,nullable=False)
    submitted_by = Column(String,nullable=False)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)

class Attendance_log(Base):
    __tablename__ = "attendance_log"

    id = Column(Integer, primary_key=True,index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    present = Column(Boolean, default=False)
    submitted_by = Column(String,nullable=False)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)
