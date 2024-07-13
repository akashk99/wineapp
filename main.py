from io import BytesIO

from fastapi import FastAPI, UploadFile, File
from PIL import Image

from MenuImageProcessor import MenuImageProcessor

app = FastAPI()


def handle_image(file_contents):
    image = Image.open(BytesIO(file_contents))

    menu_parser = MenuImageProcessor(image)
    menu_dict = menu_parser.process()

    print(menu_dict)

@app.post("/menu")
async def read_menu(file: UploadFile = File(...)):
    if file.content_type.startswith('image'):
        contents = await file.read()

        handle_image(contents)

    else:
        return {"error": "Uploaded file is not an image."}
