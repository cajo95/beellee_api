from fastapi import FastAPI
from db.db import Base, engine
from controllers.controllers import router
import models.models as pen

app = FastAPI()

pen.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/beellee", tags=["test"])