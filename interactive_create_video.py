from video_pipeline_workflow import VideoPipelineWorkflow
from models.editing_options import EditingOptions
from openai import OpenAI
from elevenlabs.client import ElevenLabs
import string
import random
import config
import os

def main():
    # Get content generation input
    subject = input("Enter the subject: ")
    
    # Ask for batch mode
    batch_mode = input("Generate multiple videos? (y/n) [default: n]: ").lower()
    if batch_mode == 'y':
        num_videos = 0
        while num_videos <= 0 or num_videos > 9:
            try:
                num_videos = int(input("How many videos to generate (1-9): "))
            except ValueError:
                print("Please enter a number between 1 and 9")
        idea_seed = None
    else:
        num_videos = 0
        idea_seed = -1
        while idea_seed < 0 or idea_seed > 9:
            try:
                idea_seed = int(input("Enter the idea seed (0-9): "))
            except ValueError:
                print("Please enter a number between 0 and 9")
    
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
        voice = "pNInz6obpgDQGcFmaJgB"  # Default ElevenLabs voice
        print("Using default ElevenLabs voice")
    
    # Get video editing input
    print("\nVideo Editing Options:")
    
    # Orientation
    orientation_options = ["vertical", "horizontal", "square"]
    orientation = input(f"Choose orientation {orientation_options} [default: vertical]: ")
    if not orientation or orientation not in orientation_options:
        print(f"Invalid orientation '{orientation}', defaulting to 'vertical'")
        orientation = "vertical"
    
    # Quality
    quality_options = ["HD", "4K", "8K"]
    quality = input(f"Choose quality {quality_options} [default: HD]: ")
    if not quality or quality not in quality_options:
        print(f"Invalid quality '{quality}', defaulting to 'HD'")
        quality = "HD"
    
    # Frame rate
    frame_rate_str = input("Enter frame rate [default: 30]: ")
    try:
        frame_rate = int(frame_rate_str) if frame_rate_str else 30
    except ValueError:
        print(f"Invalid frame rate '{frame_rate_str}', defaulting to 30")
        frame_rate = 30
    
    # Font size
    font_size_options = ["extra_small", "small", "medium", "large", "extra_large"]
    font_size = input(f"Choose font size {font_size_options} [default: extra_large]: ")
    if not font_size or font_size not in font_size_options:
        print(f"Invalid font size '{font_size}', defaulting to 'extra_large'")
        font_size = "extra_large"
    
    # Create output directories
    working_directory = os.getcwd()
    output_path = "output/video_" + ''.join(random.choices(string.ascii_letters, k=8))
    image_path = output_path + "/images"
    audio_path = output_path + "/audio"
    
    if not os.path.exists(output_path):
        os.makedirs(image_path, exist_ok=True)
        os.makedirs(audio_path, exist_ok=True)
        print(f"Created output directory: {output_path}")
    else:
        print("Directory already exists (random generation collision?), try again")
        return
    
    # Create editing options
    editing_options = EditingOptions(
        orientation=orientation,
        quality=quality,
        expected_frame_rate=frame_rate,
        font_size=font_size,
        font_stroke_width=4,
        font_stroke_color="black"
    )
    
    # Initialize the video pipeline workflow
    video_pipeline = VideoPipelineWorkflow(
        client,
        image_path,
        audio_path,
        voice,
        image_generator,
        tts_provider,
        editing_options
    )
    
    # Generate videos
    if num_videos > 0:
        final_videos = video_pipeline.batch_generate_videos(subject, num_videos)
        print(f"Generated {len(final_videos)} videos:")
        for i, video_path in enumerate(final_videos):
            print(f"{i+1}. {video_path}")
    else:
        final_video = video_pipeline.generate_complete_video(subject, idea_seed)
        print(f"Generated video: {final_video}")

if __name__ == "__main__":
    main()