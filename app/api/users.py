from fastapi import Depends, FastAPI, HTTPException,APIRouter
from app.services.db import get_db
import app.validators.schemas as schemas
from app.controller.users import UsersController
from sqlalchemy.orm import Session
from app.config import Config
from fastapi.encoders import jsonable_encoder
from app_logging import logger
from app.auth import authorize_token


config = Config()

user_router = APIRouter(prefix=f"/{config.ENVIRONMENT}/user", tags=['user'])

@user_router.post('',response_model=schemas.User,status_code=201)
async def create_user(user_request: schemas.UsersCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_user = UsersController.fetch_by_id(db, name=user_request.id)
    if db_user:
        logger.error("User already exists!")
        raise HTTPException(status_code=400, detail="User already exists!")

    return await UsersController.create(db=db, user=user_request)

@user_router.get('',response_model=schemas.User)
def get_user(user_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_user = UsersController.fetch_by_id(db,user_id)
    if db_user is None:
        logger.error("User not found with the given ID")
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    return db_user

@user_router.delete('/{user_id}')
async def delete_user(user_id: int,db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_user = UsersController.fetch_by_id(db,user_id)
    if db_user is None:
        logger.error("User not found with the given ID")
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    await UsersController.delete(db,user_id)
    return "user deleted successfully!"

@user_router.put('/{user_id}',response_model=schemas.User)
async def update_user(user_id: int,user_request: schemas.UsersCreate, db: Session = Depends(get_db),token: str = Depends(authorize_token)):
    db_user = UsersController.fetch_by_id(db, user_id)
    if db_user:
        update_user_encoded = jsonable_encoder(user_request)
        db_user.type = update_user_encoded['type']
        db_user.full_name = update_user_encoded['full_name']
        db_user.username = update_user_encoded['username']
        db_user.email = update_user_encoded['email']
        db_user.password = update_user_encoded['password']
        db_user.submitted_by = update_user_encoded['submitted_by']
        return await UsersController.update(db=db, user_data=db_user)
    else:
        raise HTTPException(status_code=400, detail="User not found with the given ID")