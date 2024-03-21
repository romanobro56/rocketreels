import concurrent.futures
import requests
import asyncio
import time
import os

class ImageProcessor:
  def __init__(self, client):
    self.client = client

  def generate_images(self, transcript, idea, image_directory_path):
    for i, sentence in enumerate(transcript):
      # FIX: ratelimiting simple workaround
      time.sleep(10)
      image_url = self.create_dalle_from_sentence(idea, sentence)
      self.download_dalle(image_url, image_directory_path, f"dalle_image_{i}.jpg")

    return str(image_directory_path)


  def create_dalle_from_sentence(self, idea, sentence):
    response = self.client.images.generate(
      model="dall-e-3",
      prompt="The image is pertaning to the topic of: " + idea + "\nCreate an image about " + sentence + " in a realistic, saturated and visually pleasing style.",
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url
  
  def download_dalle(self, image_url, image_path, filename):
    response = requests.get(image_url)
    print(response)
    if response.status_code == 200:
      full_path = os.path.join(image_path, filename)
      with open(full_path, 'wb') as file:
        file.write(response.content)
