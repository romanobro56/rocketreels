from video_generation_workflow import VideoGenerationWorkflow
from openai import OpenAI
import asyncio
import string
import random
import config
import os

# Set up OpenAI client
openai_api_key = config.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)

working_directory = os.getcwd()
output_path = "output/video_" + ''.join(random.choices(string.ascii_letters, k=8)) + "_test" # remove test when done
image_path = output_path + "/images"
audio_path = output_path + "/audio"

if not os.path.exists(output_path):
  os.makedirs(image_path, exist_ok=True)
  os.makedirs(audio_path, exist_ok=True)
  print(output_path)
else:
  print("Directory already exists (random generation collision?), try again")
  raise NameError('collision detected')



# Initialize the video generation workflow
workflow = VideoGenerationWorkflow(client, image_path, audio_path, "onyx")

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))
while idea_seed < 0 or idea_seed > 9:
  idea_seed = int(input("Please choose a number 0 through 9: "))

# Generate the video
video_clip = workflow.generate_video_content_from_idea(subject, idea_seed)
# workflow.edit_video_from_content(video_clip, output_path, output_path + "/video.mp4")