from sqlalchemy import Column, ForeignKey, Integer, String, Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

from app.services.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    type= Column(String, nullable=False)
    full_name = Column(String,nullable=False,)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    password = Column(String,nullable=False,)
    submitted_by = Column(String,nullable=False,) 
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    attendance_logs = relationship("AttendanceLog", backref="users")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    course_name= Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    semester = Column(String, nullable=False)
    class_ = Column(String, nullable=False)
    lecture_hour = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    department = relationship("Department", backref="courses")
    attendance_logs = relationship("AttendanceLog", backref="course")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    full_name = Column(String,unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"),nullable=False)
    class_ = Column(Integer, name="class")
    submitted_by = Column(String())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    department = relationship('Department', back_populates='students')
    attendance_logs = relationship('AttendanceLog', back_populates='student')


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department_name= Column(String,unique = True,nullable=False)
    submitted_by = Column(String,nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    courses = relationship('Course', back_populates='department')

class AttendanceLog(Base):
    __tablename__ = "attendance_log"

    id = Column(Integer, primary_key=True,index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    present = Column(Boolean, default=False)
    submitted_by = Column(String,nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship('User', back_populates='attendance_logs')
    course = relationship('Course', back_populates='attendance_logs')
    student = relationship('Student', back_populates='attendance_logs')