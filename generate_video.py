from video_pipeline_workflow import VideoPipelineWorkflow
from models.editing_options import EditingOptions
from openai import OpenAI
from elevenlabs.client import ElevenLabs
import string
import random
import config
import os
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate and edit a video from a subject and idea seed")
    
    # Content generation arguments
    parser.add_argument("--subject", type=str, required=True, help="Subject of the video")
    parser.add_argument("--idea-seed", type=int, default=0, help="Idea seed (0-9)")
    parser.add_argument("--batch", type=int, default=0, help="Number of videos to generate in batch mode (0 for single video)")
    parser.add_argument("--image-generator", type=str, default="openai", choices=["openai", "gemini"], help="Image generator to use")
    parser.add_argument("--tts-provider", type=str, default="openai", choices=["openai", "elevenlabs"], help="TTS provider to use")
    parser.add_argument("--voice", type=str, default="onyx", help="Voice to use for TTS")
    
    # Video editing arguments
    parser.add_argument("--orientation", type=str, default="vertical", choices=["vertical", "horizontal", "square"], help="Video orientation")
    parser.add_argument("--quality", type=str, default="HD", choices=["HD", "4K", "8K"], help="Video quality")
    parser.add_argument("--frame-rate", type=int, default=30, help="Video frame rate")
    parser.add_argument("--font-size", type=str, default="extra_large", choices=["extra_small", "small", "medium", "large", "extra_large"], help="Font size for subtitles")
    parser.add_argument("--font-stroke-width", type=int, default=4, help="Font stroke width for subtitles")
    parser.add_argument("--font-stroke-color", type=str, default="black", help="Font stroke color for subtitles")
    
    args = parser.parse_args()
    
    # Validate idea seed if not in batch mode
    if args.batch == 0 and (args.idea_seed < 0 or args.idea_seed > 9):
        print("Idea seed must be between 0 and 9")
        return
    
    # Set up OpenAI client
    openai_api_key = config.OPENAI_API_KEY
    client = OpenAI(api_key=openai_api_key)
    
    # Validate voice
    if args.tts_provider == "openai":
        openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if args.voice not in openai_voices:
            print(f"Invalid OpenAI voice '{args.voice}', defaulting to 'onyx'")
            args.voice = "onyx"
    elif args.tts_provider == "elevenlabs" and args.voice == "onyx":
        # Default ElevenLabs voice if none specified
        args.voice = "pNInz6obpgDQGcFmaJgB"
    
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
        orientation=args.orientation,
        quality=args.quality,
        expected_frame_rate=args.frame_rate,
        font_size=args.font_size,
        font_stroke_width=args.font_stroke_width,
        font_stroke_color=args.font_stroke_color
    )
    
    # Initialize the video pipeline workflow
    video_pipeline = VideoPipelineWorkflow(
        client,
        image_path,
        audio_path,
        args.voice,
        args.image_generator,
        args.tts_provider,
        editing_options
    )
    
    # Generate videos
    if args.batch > 0:
        final_videos = video_pipeline.batch_generate_videos(args.subject, args.batch)
        print(f"Generated {len(final_videos)} videos:")
        for i, video_path in enumerate(final_videos):
            print(f"{i+1}. {video_path}")
    else:
        final_video = video_pipeline.generate_complete_video(args.subject, args.idea_seed)
        print(f"Generated video: {final_video}")

if __name__ == "__main__":
    main()