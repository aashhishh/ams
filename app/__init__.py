from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from app.config import Config
from app.api.users import user_router
from app.api.attendance_log import attendance_log_router
from app.api.courses import course_router
from app.api.department import department_router
from app.api.students import students_router
from app_logging import logger

config = Config()

middlewares = [
    Middleware(CORSMiddleware,
               allow_origins=['*'],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"]
               )
]

AMS = FastAPI(debug=True if Config.ENVIRONMENT in ["LOCAL"] else False, middleware=middlewares)
     
AMS.include_router(attendance_log_router)
AMS.include_router(course_router)
AMS.include_router(students_router)
AMS.include_router(department_router)
AMS.include_router(user_router)


if __name__ == "app":
    logger.info(f"[START]: {Config.APP_NAME} running in {Config.ENVIRONMENT}")