import json
from io import BytesIO

from fastapi import FastAPI, UploadFile, File
from PIL import Image

from menu_image_processor import WineMenuImageProcessor
from wine_api_client import WineAPIClient
from wine_details import WineDetails

app = FastAPI()


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
