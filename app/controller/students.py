from sqlalchemy.orm import Session
from app.models import models
from app.validators import schemas

class StudentsController:
    def create(db: Session, student: schemas.StudentsCreate):
        db_student = models.Students(full_name=student.full_name,
                               semester=student.semester,
                               class_=student.class_,
                               submitted_by=student.submitted_by)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    def fetch_by_id(db: Session,_id):
        return db.query(models.Students).filter(models.Students.id == _id).first()
 
    def fetch_by_name(db: Session,name):
        return db.query(models.Students).filter(models.Students.full_name == name).first()
 
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Students).offset(skip).limit(limit).all()

    def update(db: Session,student_data):
        updated_student = db.merge(student_data)
        db.commit()
        return updated_student