from sqlalchemy.orm import Session
from app.models import models
from app.validators import schemas

class DepartmentController:
    def create(db: Session, user: schemas.DepartmentCreate):
        db_user = models.Departments(department_name=user.department_name,
                                     submitted_by=user.submitted_by)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def fetch_by_id(db: Session,_id):
        return db.query(models.Departments).filter(models.Departments.id == _id).first()
 
    def fetch_by_name(db: Session,name):
        return db.query(models.Departments).filter(models.Departments.name == name).first()
 
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Departments).offset(skip).limit(limit).all()

    def update(db: Session,user_data):
        updated_user = db.merge(user_data)
        db.commit()
        return updated_user