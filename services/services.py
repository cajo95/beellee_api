from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models.models import Purchases, Users
from dotenv import load_dotenv
from requests import HTTPError
from datetime import datetime
from openai import OpenAI
from db.db import engine
#from fastapi import HTTPException IMPORTANTE MANEJAR LA EXCEPCIÓN HTTP DE LOS ENDPOINTS
#import numpy as np
import requests
import uuid
import json
import os

load_dotenv(".env")

class purchases():

  def scanner_image(self, _base64_image):
    api_key=os.environ.get("OPENAI_API_KEY")
    #client = OpenAI(api_key)
    try:
      headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
      }

      payload = {
        "model": "gpt-4o-mini",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": """Analyze the following image. If it contains an invoice or purchase receipt, return just a JSON with the name of the establishment,
                the list of items purchased, their respective unit prices, and the total paid value of the invoice in the following format: 
                {\"establishment\": \"\", \"items\": [{\"name\": \"\", \"unit_price\": , \"quantity\": , \"total_price\": }], \"total_invoice_value\": }.
                If the image does not contain an invoice or receipt, return 'FALSE'. If any required data is missing, replace it with 'N/A'. 
                Ensure all extracted text is returned in UPPER CASE."""
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{_base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 900  # Ajusta este valor según tus necesidades
      }
        #RECORDARLE LA MODELO QUE DEBE RETORNAR LOS VALORES EN MONEDA COLOMBIANA EN MILES DE PESOS. DARLE VARIOS EJEMPLOS.
      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      response_dict = response.json()
      content = response_dict["choices"][0]["message"]["content"]
      #print(content)

      if len(content) > 0:
        if content != 'FALSE':
          content_cleaned = content.replace('```json', '').replace('```', '').strip()
          try:
              json_object = json.loads(content_cleaned)
              #json_object_response = json.dumps(json_object, indent=2, ensure_ascii=False)
              return json_object
          except json.JSONDecodeError:
              return content_cleaned
        else:
            return False
      else:
          return False
      
    except Exception as e:
      #print('Error:', e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

  def save_purchase_data(self, json_purchese, db):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      #purchase = session.query(Purchases).filter(Purchases.purchese_code == purchese_code).first()
      print(json_purchese)
      # new_purchase = Purchases(
      #   purchese_code=str(uuid.uuid4()),
      #   establishment=json_purchese["establishment"],
      #   total_invoice_value=json_purchese["total_invoice_value"],
      #   items=json_purchese["items"],
      #   created_at=datetime.now()
      # )
      return True
    except Exception as e:
      print('Error:', e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    # finally:
    #   session.close()


  # def new_users(self, user_data, db):
  #     try:
  #         print(user_data)
  #         new_user = Users(
  #             user_code=user_data["user_id"],
  #             user_name=user_data["username"],
  #             name=user_data["name"],
  #             surname=user_data["surname"],
  #             identification=user_data["user_id"],
  #             country=user_data["country"],
  #             city=user_data["city"],
  #             address=user_data.get("address", ''),
  #             email=user_data["email"],
  #             phone=user_data["phone"],
  #             activity=user_data["activity"],
  #             activity_type_id=user_data["type_activity"],
  #             income_type_id=user_data["first_income"],
  #             activated=user_data.get("activated", False)
  #         )

  #         db.add(new_user)
  #         db.commit()
  #         db.refresh(new_user)  # Refrescar para obtener el ID y otros campos generados
  #         db.close()
  #         print('prueba')
  #         return new_user
  #     except SQLAlchemyError as e:
  #         db.rollback()  # Revertir la transacción en caso de error
  #         print(f"Error al insertar el usuario: {e}")
  #         return None

# TODO: DESARROLLAR UN CONTADOR DE TOKKENS PARA QUE NO SEA UN NUMERO FIJO SINO QUE VAYA JUSTON CON LO QUE SE NECESITA (SUPER IMPORTANTE)
# TODO: Tener en cuenta Casos especiales
# TODO: Guardar imagen en base de datos como base64 para que el usuario tenga acceso a ella en cualquier momento.
# TODO: Ver si se puede configuar el bot de telegram para que tome fotos de 512px x 512px.
# TODO: Traajar en el control de errores http tanto en api como en bot.

# NEW TODO:
# TODO: Cambiar user_id de intero a string
# TODO: Cambiar em item purchase_id por porchese_code o algo así: hacer un nuevo campo nuevo en purchase para relacionarlo con item
