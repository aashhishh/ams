from fastapi import Depends, FastAPI, HTTPException,APIRouter
from fastapi.responses import JSONResponse
from app.services.db import get_db
import app.validators.schemas as schemas
from app.controller.students import StudentsController
from sqlalchemy.orm import Session
from app.config import Config
from app_logging import logger
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from app.auth import authorize_token

config = Config()

students_router = APIRouter(prefix=f"/{config.ENVIRONMENT}/students", tags=['students'])

@students_router.post('',response_model=schemas.Students,status_code=201)
async def create_student(student_request: schemas.StudentsCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_student = StudentsController.fetch_by_id(db, name=token.id)
    if db_student:
        logger.error("Students already exists!")
        raise HTTPException(status_code=400, detail="Students already exists!")

    return await StudentsController.create(db=db, student=student_request)

@students_router.get('',response_model=schemas.Students)
def get_student(student_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_student = StudentsController.fetch_by_id(db,student_id)
    if db_student is None:
        logger.error("Students not found with the given ID")
        raise HTTPException(status_code=404, detail="Students not found with the given ID")
    return db_student

@students_router.delete('/{student_id}')
async def delete_student(student_id: int,db: Session = Depends(get_db)):
    db_student = StudentsController.fetch_by_id(db,student_id)
    if db_student is None:
        logger.error("Students not found with the given ID")
        raise HTTPException(status_code=404, detail="Students not found with the given ID")
    await StudentsController.delete(db,student_id)
    return "student deleted successfully!"

@students_router.put('/{student_id}',response_model=schemas.Students)
async def update_student(student_id: int,student_request: schemas.StudentsCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_student = StudentsController.fetch_by_id(db, student_id)
    if db_student:
        update_user_encoded = jsonable_encoder(student_request)
        db_student.full_name = update_user_encoded['full_name']
        db_student.semester = update_user_encoded['semester']
        db_student.class_ = update_user_encoded['class_']
        db_student.submitted_by = update_user_encoded['submitted_by']
        return await StudentsController.update(db=db, user_data=db_student)
    else:
        logger.error("Students not found with the given ID")
        raise HTTPException(status_code=400, detail="Students not found with the given ID")