from content_generation_workflow import ContentGenerationWorkflow
from openai import OpenAI
import jsonpickle
import asyncio
import string
import random
import config
import pickle
import json
import os

# Set up OpenAI client
openai_api_key = config.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)

working_directory = os.getcwd()
output_path = "output/video_" + ''.join(random.choices(string.ascii_letters, k=8)) + "_test" # remove test when done
image_path = output_path + "/images"
audio_path = output_path + "/audio"
video_clip_path = output_path + "/video_clip"

if not os.path.exists(output_path):
  os.makedirs(image_path, exist_ok=True)
  os.makedirs(audio_path, exist_ok=True)
  os.makedirs(video_clip_path, exist_ok=True)
  print(output_path)
else:
  print("Directory already exists (random generation collision?), try again")
  raise NameError('collision detected')

# Initialize the video generation workflow
content_generation_workflow = ContentGenerationWorkflow(client, image_path, audio_path, "onyx")

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))
while idea_seed < 0 or idea_seed > 9:
  idea_seed = int(input("Please choose a number 0 through 9: "))

# Generate the video
video_clip = content_generation_workflow.generate_video_content_from_idea(subject, idea_seed)

def save_object(obj, video_clip_path):
    with open(video_clip_path + "/video_clip.pkl", 'wb') as outp:  # Write in binary mode
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

# Function to load and deserialize the object from a file
def load_object(filename):
    with open(filename, 'rb') as inp:  # Read in binary mode
        return pickle.load(inp)
    
save_object(video_clip, video_clip_path)
