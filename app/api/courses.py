from fastapi import Depends, FastAPI, HTTPException,APIRouter
from fastapi.responses import JSONResponse
from app.services.db import get_db
import app.validators.schemas as schemas
from app.controller.courses import CoursesController
from sqlalchemy.orm import Session
from app.config import Config
from app_logging import logger
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from app.auth import authorize_token

config = Config()

course_router = APIRouter(prefix=f"/{config.ENVIRONMENT}/course", tags=['course'])

@course_router.post('',response_model=schemas.Courses,status_code=201)
async def create_course(course_request: schemas.CoursesCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_course = CoursesController.fetch_by_id(db, name=course_request.id)
    if db_course:
        logger.error("Courses already exists!")
        raise HTTPException(status_code=400, detail="Courses already exists!")

    return await CoursesController.create(db=db, course=course_request)

@course_router.get('',response_model=schemas.Courses)
def get_course(course_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_course = CoursesController.fetch_by_id(db,course_id)
    if db_course is None:
        logger.error("Courses not found with the given ID")
        raise HTTPException(status_code=404, detail="Courses not found with the given ID")
    return db_course

@course_router.delete('/{course_id}')
async def delete_course(course_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_course = CoursesController.fetch_by_id(db,course_id)
    if db_course is None:
        logger.error("Courses not found with the given ID")
        raise HTTPException(status_code=404, detail="Courses not found with the given ID")
    await CoursesController.delete(db,course_id)
    return "student deleted successfully!"

@course_router.put('/{course_id}',response_model=schemas.Courses)
async def update_course(course_id: int,course_request: schemas.CoursesCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_course = CoursesController.fetch_by_id(db, course_id)
    if db_course:
        update_course_encoded = jsonable_encoder(course_request)
        db_course.course_name = update_course_encoded['course_name']
        db_course.semester = update_course_encoded['semester']
        db_course.class_ = update_course_encoded['class_']
        db_course.lecture_hour = update_course_encoded['lecture_hour']
        db_course.submitted_by = update_course_encoded['submitted_by']
        return await CoursesController.update(db=db, course_data=db_course)
    else:
        logger.error("Courses not found with the given ID")
        raise HTTPException(status_code=400, detail="Courses not found with the given ID")