from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from models.models import Purchases, Items
from dotenv import load_dotenv
from requests import HTTPError
from datetime import datetime
from openai import OpenAI
from db.db import engine
from fastapi import HTTPException, status
#import numpy as np
import requests
import uuid
import json
import os

load_dotenv(".env")

class purchases():

  def scanner_image(self, _base64_image):
    global data_base64_image
    data_base64_image = _base64_image 

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

  def save_purchase_data(self, json_purchase, db):
      data_number_items = len(json_purchase['purchase_data']['items'])
      try:
          # Create new purchase record
          new_purchase = Purchases(
              user_code='81380774',
              purchese_code=str(uuid.uuid4()),
              number_items=data_number_items,
              establishment=json_purchase['purchase_data']["establishment"],
              type_id=8,
              total_payment=json_purchase['purchase_data']["total_invoice_value"],
              invoice_B64=data_base64_image
          )
          
          db.add(new_purchase)
          db.commit()
          
          # Add items with correct data structure access
          for item in json_purchase['purchase_data']["items"]:
              new_item = Items(
                  purchese_code=new_purchase.purchese_code,
                  name=item["name"],
                  value=item["unit_price"],
                  quantity=item["quantity"],
                  type_id=1
              )
              db.add(new_item)
          
          db.commit()
          db.refresh(new_purchase)
          
          return True
      
      except SQLAlchemyError as e:
          db.rollback()
          raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Database error: {str(e)}"
          )
# TODO: DESARROLLAR UN CONTADOR DE TOKKENS PARA QUE NO SEA UN NUMERO FIJO SINO QUE VAYA JUSTON CON LO QUE SE NECESITA (SUPER IMPORTANTE)
# TODO: Tener en cuenta Casos especiales
# TODO: Guardar imagen en base de datos como base64 para que el usuario tenga acceso a ella en cualquier momento.
# TODO: Ver si se puede configuar el bot de telegram para que tome fotos de 512px x 512px.