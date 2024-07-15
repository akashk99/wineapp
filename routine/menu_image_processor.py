import json

import pytesseract
from PIL import ImageFilter, ImageEnhance
from openai import OpenAI
import os

from routine.custom_functions import CustomFunctions
from payload.wine_menu_item import WineMenuItem


class WineMenuImageProcessor:

    def __init__(self, image):
        self.image = image
        self.open_ai_client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
        )

    def process(self):
        self.__preprocess_image()
        text = pytesseract.image_to_string(image=self.image)
        return self.__process_raw_wine_list(text)

    def __preprocess_image(self):
        # Convert the image to grayscale
        self.image = self.image.convert('L')

        # Resize the image to enhance OCR accuracy (avoid excessive resizing)
        width, height = self.image.size
        self.image = self.image.resize((int(width * 1.5), int(height * 1.5)))

        # Enhance contrast (moderate enhancement)
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1.5)

        # Optional: Apply a light sharpening filter
        self.image = self.image.filter(ImageFilter.SHARPEN)



    def __process_raw_wine_list(self, text):
        response = self.open_ai_client.chat.completions.create(
            model='gpt-4o',
            temperature=0.05,
            messages=[
                {'role': 'user', 'content': f'extract the following menu text into a structured JSON format. Ensure '
                                            f'that the year is always a 4-digit number. When both glass and bottle '
                                            f'prices are available, use the bottle price.\n\nMenu Text:\n{text}'}
            ],
            tool_choice='required',
            tools=[{
                "type": "function",
                "function": CustomFunctions.extract_wine_function
            }],
        )

        json_response = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        wines = [WineMenuItem(**wine) for wine in json_response['wines']]

        return wines



