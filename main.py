from video_generation_workflow import VideoGenerationWorkflow
from openai import OpenAI
import asyncio
import config
import os

# Set up OpenAI client
openai_api_key = config.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)

working_directory = os.getcwd()
output_directory = working_directory + "/test"

if not os.path.exists(output_directory):
  os.makedirs(output_directory)

print(output_directory)


# Initialize the video generation workflow
workflow = VideoGenerationWorkflow(client, output_directory, "onyx")

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))
while idea_seed < 0:
  idea_seed = int(input("Please choose a number 0 through 9 "))

# Generate the video
asyncio.run(workflow.generate_video_from_idea(subject, idea_seed))