import app.models.models as models
from app.services.db import engine


models.Base.metadata.create_all(bind=engine)