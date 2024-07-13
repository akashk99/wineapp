import pytesseract

class MenuProcessor:
    def __init__(self, image):
        self.image = image


    def process(self):
        print(pytesseract.image_to_string(self.image))

    def __preprocess_image(self):
        pass
