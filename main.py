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
output_path = "output/video_" + ''.join(random.choices(string.ascii_letters, k=8)) + "_test"

if not os.path.exists(output_path):
  os.makedirs(output_path)
else:
  print("Directory already exists, try again")

print(output_path)


# Initialize the video generation workflow
workflow = VideoGenerationWorkflow(client, output_path, "onyx")

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))
while idea_seed < 0:
  idea_seed = int(input("Please choose a number 0 through 9 "))

# Generate the video
workflow.generate_video_from_idea(subject, idea_seed)