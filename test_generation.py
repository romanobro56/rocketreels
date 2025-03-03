from content_generation_workflow import ContentGenerationWorkflow
from utils.utilities import save_object
from openai import OpenAI
from elevenlabs.client import ElevenLabs
import string
import random
import config
import pickle
import os

# Get user input
subject = input("Enter the subject: ")
idea_seed = int(input("Enter the idea seed: "))
while idea_seed < 0 or idea_seed > 9:
  idea_seed = int(input("Please choose a number 0 through 9: "))

# Ask user which image generator to use
image_generator = input("Choose image generator (openai/gemini) [default: openai]: ").lower()
if image_generator not in ["openai", "gemini"]:
  print(f"Invalid choice '{image_generator}', defaulting to 'openai'")
  image_generator = "openai"

# Ask user which TTS provider to use
tts_provider = input("Choose TTS provider (openai/elevenlabs) [default: openai]: ").lower()
if tts_provider not in ["openai", "elevenlabs"]:
  print(f"Invalid choice '{tts_provider}', defaulting to 'openai'")
  tts_provider = "openai"

# Set up OpenAI client
openai_api_key = config.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)

# Initialize ElevenLabs client if needed
elevenlabs_client = None
if tts_provider == "elevenlabs":
  elevenlabs_client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)

# Get voice based on the selected TTS provider
if tts_provider == "openai":
  # List available OpenAI voices
  openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
  print("Available OpenAI voices:", ", ".join(openai_voices))
  voice = input(f"Choose an OpenAI voice [default: onyx]: ")
  if not voice or voice not in openai_voices:
    print(f"Invalid OpenAI voice '{voice}', defaulting to 'onyx'")
    voice = "onyx"
else:  # elevenlabs
  voice = "pNInz6obpgDQGcFmaJgB"

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
content_generation_workflow = ContentGenerationWorkflow(
  client, 
  image_path, 
  audio_path, 
  voice, 
  image_generator,
  tts_provider
)

# Generate the video
video_clip = content_generation_workflow.generate_video_content_from_idea(subject, idea_seed)
    
save_object(video_clip, "video_clip", video_clip_path)