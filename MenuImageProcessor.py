import pytesseract


class MenuImageProcessor:
    def __init__(self, image):
        self.image = image

    def process(self): # will return a dict of wines and prices
        print(pytesseract.image_to_string(self.image))

    def __preprocess_image(self):
        pass
