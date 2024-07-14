import json
import os
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, Form, requests
from PIL import Image
from twilio.twiml.messaging_response import MessagingResponse

from menu_image_processor import WineMenuImageProcessor
from wine_api_client import WineAPIClient
from wine_details import WineDetails
import requests
from twilio.rest import Client

app = FastAPI()

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# twilio_phone_number = '+14318147282'
#
# twilio_client = Client(account_sid, auth_token)

def handle_image(file_contents):
    image = Image.open(BytesIO(file_contents))

    menu_parser = WineMenuImageProcessor(image)
    wine_list = menu_parser.process()

    wine_api_client = WineAPIClient()

    wine_details_list = []
    for wine in wine_list:
        wine_details = wine_api_client.lookup_wine(wine)
        if wine_details:
            wine_details_list.append(wine_details)

    wine_details_list.sort(key=lambda x: (x.rating, x.rating_count), reverse=True)

    return wine_details_list


@app.post("/menu")
async def read_menu(file: UploadFile = File(...)):
    if file.content_type.startswith('image'):
        contents = await file.read()

        return handle_image(contents)

    else:
        return {"error": "Uploaded file is not an image."}

@app.get("/")
async def home():
    return "hi"


# @app.post("/sms")
# async def read_menu_from_sms(
#         NumMedia: int = Form(0),
#         MediaUrl0: str = Form(None),
# ):
#     response = MessagingResponse()
#
#     if NumMedia > 0:
#         media_url = MediaUrl0
#         img_data = requests.get(media_url).content
#
#         wine_details_list = handle_image(img_data)
#
#         print(wine_details_list)
#
#         twilio_client.messages.create(
#             body='Hello, this is a test message from Twilio!',
#             from_=twilio_phone_number,  # Your Twilio number
#             to='+16506461633'      # The recipient's number
#         )
#
#         return str(response)
#
#     else:
#         return {"error": "Uploaded file is not an image."}
