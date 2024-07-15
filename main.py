from io import BytesIO

import requests
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

from routine.menu_image_processor import WineMenuImageProcessor
from routine.wine_detail_fetcher import WineDetailFetcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def handle_image(file_contents):
    image = Image.open(BytesIO(file_contents))

    menu_parser = WineMenuImageProcessor(image)
    wine_list = menu_parser.process()

    wine_detail_fetcher = WineDetailFetcher()

    wine_details_list = []
    for wine in wine_list:
        wine_details = wine_detail_fetcher.get_wine_details(wine)
        if wine_details:
            wine_details_list.append(wine_details)

    wine_details_list.sort(key=lambda x: (x.rating, x.rating_count), reverse=True)

    return wine_details_list


@app.post("/menu")
async def read_menu(file: UploadFile = File(...)):
    if file.content_type.startswith('image'):
        contents = await file.read()

        wine_details_list = handle_image(contents)

        return wine_details_list

    else:
        return {"error": "Uploaded file is not an image."}


@app.get("/")
async def read_root():
    return {"Hello": "World"}

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# twilio_phone_number = '+14318147282'
#
# twilio_client = Client(account_sid, auth_token)


@app.post("/sms")
async def read_menu_from_sms(
        NumMedia: int = Form(0),
        MediaUrl0: str = Form(None),
):

    if NumMedia > 0:
        media_url = MediaUrl0
        # print(media_url)
        img_data = requests.get(media_url).content

        wine_details_list = handle_image(img_data)

        print(wine_details_list)

    else:
        return {"error": "Uploaded file is not an image."}
