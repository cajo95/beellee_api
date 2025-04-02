import requests
from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from db.db import SessionLocal
from pydantic import BaseModel
from services.services import purchases
from sqlalchemy.orm import Session
import base64
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Imagen(BaseModel):
    image_base64: str

@router.post("/upload/image/")
async def upload_image(imagen: Imagen, db: Session = Depends(get_db)):
    
    try:
        image_base64 = imagen.image_base64
        _answer = purchases().scanner_image(image_base64)

        if isinstance(_answer, dict):
            return _answer
        else:
            return False 

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post("/accepted-purchase/")
async def save_accepted_purchase(data_purchase: dict, db: Session = Depends(get_db)):
    try:
        purchase_data = purchases().save_purchase_data(data_purchase, db)
        return purchase_data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# @router_pensar.get("/competencies", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={   
#                     200: {"description": "Successful Response"},
#                     404: {"description": "Resource not found"},
#                     500: {"description": "Internal Server Error"}
#                 })
# async def competences(code: int, year: int, 
#                     grade: Union[int, None] = None, 
#                     classroom: Union[str, None] = None, 
#                     idCompetence: Union[int, None] = None, 
#                     idArea: Union[int, None] = None, 
#                     db: Session = Depends(get_db)):
    
#     _competencia = Ppensar().competences_calculate(code, year, grade, classroom, idCompetence, idArea, db)
#     # if not _competencia:
#     #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencie not found")
#     return _competencia