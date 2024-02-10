import os
from openai import OpenAI
from video_generation_workflow import VideoGenerationWorkflow

# Set up OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Initialize the video generation workflow
workflow = VideoGenerationWorkflow(client)

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))

# Generate the video
workflow.generate_video_from_idea(subject, idea_seed)