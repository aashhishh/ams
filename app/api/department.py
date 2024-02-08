from fastapi import Depends, FastAPI, HTTPException,APIRouter
from fastapi.responses import JSONResponse
from app.services.db import get_db
import app.validators.schemas as schemas
from app.controller.departments import DepartmentController
from sqlalchemy.orm import Session
from app.config import Config
from app_logging import logger
from typing import List,Optional
from app.auth import authorize_token
from fastapi.encoders import jsonable_encoder


config = Config()

department_router = APIRouter(prefix=f"/{config.ENVIRONMENT}/department", tags=['department'])

@department_router.post('',response_model=schemas.Department,status_code=201)
async def create_department(department_request: schemas.DepartmentCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_department = DepartmentController.fetch_by_id(db, name=department_request.id)
    if db_department:
        logger.error("Department already exists!")
        raise HTTPException(status_code=400, detail="Department already exists!")

    return await DepartmentController.create(db=db, student=department_request)

@department_router.get('',response_model=schemas.Department)
def get_department(student_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_department = DepartmentController.fetch_by_id(db,student_id)
    if db_department is None:
        logger.error("Department not found with the given ID")
        raise HTTPException(status_code=404, detail="Department not found with the given ID")
    return db_department

@department_router.delete('/{student_id}')
async def delete_department(student_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_department = DepartmentController.fetch_by_id(db,student_id)
    if db_department is None:
        logger.error("Department not found with the given ID")
        raise HTTPException(status_code=404, detail="Department not found with the given ID")
    await DepartmentController.delete(db,student_id)
    return "student deleted successfully!"

@department_router.put('/{student_id}',response_model=schemas.Department)
async def update_department(student_id: int,department_request: schemas.DepartmentCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_department = DepartmentController.fetch_by_id(db, student_id)
    if db_department:
        update_user_encoded = jsonable_encoder(department_request)
        db_department.full_name = update_user_encoded['full_name']
        db_department.semester = update_user_encoded['semester']
        db_department.class_ = update_user_encoded['class_']
        db_department.submitted_by = update_user_encoded['submitted_by']
        return await DepartmentController.update(db=db, user_data=db_department)
    else:
        logger.error("Department not found with the given ID")
        raise HTTPException(status_code=400, detail="Department not found with the given ID")