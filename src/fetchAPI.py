import requests 
import random
from dotenv import load_dotenv
from PIL import ImageTk, Image
from io import BytesIO
import tkinter as tk
import os
class FetchAPI():
        query: str
        quantity: int
        img_width: int
        img_height: int
        load_dotenv()
        api_key = os.getenv('PEXELS_API_KEY')
        def __init__(self, query: str, quantity: int) -> None:
                self.img_width = 1280
                self.img_height = 720
                self.query = query
                self.quantity = quantity

        # Getter Method
        def get_query(self):
                return self.query
        def get_quantity(self):
                return self.quantity
        # Setter Method
        def set_query(self, newQuery):
                self.query = newQuery
        def set_quantity(self, newQuantity):
                self.query = newQuantity

        @staticmethod
        def randomNumber() -> int:
                return random.randint(1, 100)
	
        def fetchAPI(self):
                url = f'https://api.pexels.com/v1/search?query={self.get_query()}&per_page={self.get_quantity()}&page={self.randomNumber()}&orientation=landscape'
                headers = {'Authorization': self.api_key}
                response = requests.get(url, headers=headers)
                return response.json()
                
        def DisplayPhotos(self)-> None:
                data = self.fetchAPI()
                for photo in data['photos']:
                        photo_link = photo['src']['medium']
                        response = requests.get(photo_link)
                        image = Image.open(BytesIO(response.content))
                        root = tk.Tk()
                        root.wm_attributes("-topmost", 1)
                        tk_image = ImageTk.PhotoImage(image)
                        label = tk.Label(root, image=tk_image, text= self.get_query())
                        label.pack()
                        root.mainloop()
                return None
