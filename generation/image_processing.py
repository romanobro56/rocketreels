import concurrent.futures
import requests
import asyncio
import os

class ImageProcessor:
  def __init__(self, client):
    self.client = client

  async def generate_images(self, transcript, idea, image_directory_path):
    os.makedirs(image_directory_path, exist_ok=True)

    async def download_image(i, sentence):
      loop = asyncio.get_running_loop()
      # Run the blocking API call in a thread pool
      image_url = await loop.run_in_executor(None, self.create_dalle_from_sentence, idea, sentence)
      # Now, download the image
      self.download_dalle(image_url, image_directory_path, f"dalle_image_{i}.jpg")

    async with asyncio.TaskGroup() as tg:
      for i, sentence in enumerate(transcript):
        tg.create_task(download_image(i, sentence))

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
