from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import concurrent.futures
import requests
import time
import os
import math

class GeminiImageProcessor:
  def __init__(self, api_key):
    self.client = genai.Client(api_key=api_key)
    self.rate_limit = 5  # Images per minute limit
    
  def generate_images(self, transcript, idea, image_directory_path):
    if not os.path.exists(image_directory_path):
      os.makedirs(image_directory_path, exist_ok=True)
    
    # Calculate how many batches we need (ceil to handle partial batches)
    total_images = len(transcript)
    num_batches = math.ceil(total_images / self.rate_limit)
    
    print(f"Processing {total_images} images in {num_batches} batches...")
    
    successful_images = set()
    
    # Process in batches of 5 images (rate limit)
    for batch_num in range(num_batches):
      start_idx = batch_num * self.rate_limit
      end_idx = min(start_idx + self.rate_limit, total_images)
      batch_indices = list(range(start_idx, end_idx))
      
      print(f"Starting batch {batch_num+1}/{num_batches} (images {start_idx} to {end_idx-1})")
      
      # Process current batch with parallel execution
      with concurrent.futures.ThreadPoolExecutor(max_workers=self.rate_limit) as executor:
        # Submit all tasks in this batch
        future_to_index = {
          executor.submit(
            self.create_and_download_image, 
            idea, 
            transcript[i], 
            image_directory_path, 
            i
          ): i for i in batch_indices if i not in successful_images
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_index.keys()):
          index = future_to_index[future]
          try:
            future.result()
            successful_images.add(index)
            print(f"Image {index} completed successfully")
          except Exception as e:
            print(f"Image {index} generation failed: {e}")
      
      # Wait for rate limit reset before starting next batch
      # But don't wait after the final batch
      if batch_num < num_batches - 1:
        print(f"Waiting 60 seconds before next batch...")
        time.sleep(60)  # Wait a full minute between batches
    
    # Check for any failed images and retry them one more time
    failed_indices = set(range(total_images)) - successful_images
    if failed_indices:
      print(f"Retrying {len(failed_indices)} failed images...")
      time.sleep(60)  # Wait before retry
      
      for index in failed_indices:
        try:
          self.create_and_download_image(idea, transcript[index], image_directory_path, index)
          print(f"Image {index} retry successful")
        except Exception as e:
          print(f"Image {index} retry failed: {e}")
          
    print(f"Image generation completed: {len(successful_images)}/{total_images} successful")
    return str(image_directory_path)
  
  def create_and_download_image(self, idea, sentence, image_directory_path, index):
    # Add small staggered delay (1-2 seconds) to avoid exact simultaneous requests
    time.sleep(1 + (index % 2))
    
    # Generate the image
    image_bytes = self.create_gemini_from_sentence(idea, sentence)
    
    # Save the image directly
    self.save_image(image_bytes, image_directory_path, f"dalle_image_{index}.jpg")
    
    return index

  def create_gemini_from_sentence(self, idea, sentence):
    try:
      prompt = f"The image is pertaining to the topic of: {idea}\nCreate an image about {sentence} in a realistic, saturated and visually pleasing style."
      
      response = self.client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        )
      )
      
      # Return the image bytes from the first (and only) generated image
      return response.generated_images[0].image.image_bytes
    except Exception as e:
      print(f"Error generating image: {e}")
      raise
  
  def save_image(self, image_bytes, image_path, filename):
    try:
      full_path = os.path.join(image_path, filename)
      image = Image.open(BytesIO(image_bytes))
      image.save(full_path, format="JPEG")
      print(f"Saved image: {filename}")
    except Exception as e:
      raise Exception(f"Failed to save image: {e}")