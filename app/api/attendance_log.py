from fastapi import Depends, FastAPI, HTTPException,APIRouter
from app.services.db import get_db
import app.validators.schemas as schemas
from app.controller.attendance_log import Attendance_logController
from sqlalchemy.orm import Session
from app.config import Config
from app_logging import logger
from fastapi.encoders import jsonable_encoder
from app.auth import authorize_token

config = Config()

attendance_log_router = APIRouter(prefix=f"/{config.ENVIRONMENT}/attendance_log", tags=['attendance_log'])

@attendance_log_router.post('',response_model=schemas.Attendance_log,status_code=201)
async def create_attendance_log(attendance_log_request: schemas.Attendance_logCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_attendance_log = Attendance_logController.fetch_by_id(db, name=attendance_log_request.id)
    if db_attendance_log:
        logger.error("Attandance_log already exists!")
        raise HTTPException(status_code=400, detail="Attandance_log already exists!")

    return await Attendance_logController.create(db=db, student=attendance_log_request)

@attendance_log_router.get('',response_model=schemas.Attendance_log)
def get_attendance_log(attandance_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_attendance_log = Attendance_logController.fetch_by_id(db,attandance_id)
    if db_attendance_log is None:
        logger.error("Attandance_log not found with the given ID")
        raise HTTPException(status_code=404, detail="Attandance_log not found with the given ID")
    return db_attendance_log

@attendance_log_router.delete('/{attandance_id}')
async def delete_attendance_log(attandance_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_attendance_log = Attendance_logController.fetch_by_id(db,attandance_id)
    if db_attendance_log is None:
        logger.error("Attandance_log not found with the given ID")
        raise HTTPException(status_code=404, detail="Attandance_log not found with the given ID")
    await Attendance_logController.delete(db,attandance_id)
    return "Attandance_log deleted successfully!"

@attendance_log_router.put('/{attandance_id}',response_model=schemas.Attendance_log)
async def update_attendance_log(attandance_id: int,attendance_log_request: schemas.Attendance_logCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_attendance_log = Attendance_logController.fetch_by_id(db, attandance_id)
    if db_attendance_log:
        update_user_encoded = jsonable_encoder(attendance_log_request)
        db_attendance_log.present = update_user_encoded['present']
        db_attendance_log.submitted_by = update_user_encoded['submitted_by']
        return await Attendance_logController.update(db=db, user_data=db_attendance_log)
    else:
        logger.error("Attandance_log not found with the given ID")
        raise HTTPException(status_code=400, detail="Attandance_log not found with the given ID")