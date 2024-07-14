import json

import pytesseract
from PIL import ImageFilter, ImageEnhance
from PIL.Image import Image
from openai import OpenAI
import os

from custom_functions import CustomFunctions
from winemenuitem import WineMenuItem


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
        self.image = self.image.convert('L')
        threshold = 128
        self.image = self.image.point(lambda p: p > threshold and 255)

        # Resize the image to enhance OCR accuracy
        width, height = self.image.size
        self.image = self.image.resize((width * 2, height * 2))

        self.image = self.image.filter(ImageFilter.GaussianBlur(1))

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(2)

        # Optionally apply other filters
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



