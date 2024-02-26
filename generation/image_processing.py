import requests
import os

class ImageProcessor:
  def __init__(self, client):
    self.client = client

  def generate_images(self, client, transcript, idea, image_directory_path):
    for i, sentence in enumerate(transcript):
      image_url = self.create_dalle_from_sentence(client, idea, sentence)
      self.download_dalle(image_url, image_directory_path, f"dalle_image_{i}.jpg")

    return str(image_directory_path)

  def create_dalle_from_sentence(self, client, idea, sentence):
    response = client.images.generate(
      model="dall-e-3",
      prompt="The image is pertaning to the topic of: " + idea + "\nCreate an image about " + sentence + " in a realistic, saturated and visually pleasing style.",
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url
  
  def download_dalle(self, image_url, image_path, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        full_path = os.path.join(image_path, filename)
        with open(full_path, 'wb') as file:
            file.write(response.content)
