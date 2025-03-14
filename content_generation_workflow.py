from models.multimedia_composition import MultimediaComposition
from editing.subtitle_processing import SubtitleProcessor
from generation.image_processing import ImageProcessor
from generation.gemini_image_processor import GeminiImageProcessor
from generation.audio_processing import AudioProcessor
from generation.text_processing import TextProcessor
from elevenlabs.client import ElevenLabs
import concurrent.futures
import config
import os

class ContentGenerationWorkflow:
  def __init__(self, client, image_path, audio_path, voice, image_generator="openai", tts_provider="openai"):
    self.subtitle_processor = SubtitleProcessor(client)
    
    # Initialize ElevenLabs client if needed
    self.elevenlabs_client = None
    if tts_provider.lower() == "elevenlabs":
      self.elevenlabs_client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
    
    # Initialize audio processor with both clients
    self.audio_processor = AudioProcessor(client, self.elevenlabs_client)
    
    # Initialize the selected image processor
    if image_generator.lower() == "openai":
      self.image_processor = ImageProcessor(client)
    elif image_generator.lower() == "gemini":
      self.image_processor = GeminiImageProcessor(config.GEMINI_API_KEY)
    else:
      raise ValueError(f"Unsupported image generator: {image_generator}. Use 'openai' or 'gemini'")
      
    self.text_processor = TextProcessor(client)
    self.image_path = image_path
    self.audio_path = audio_path
    self.client = client
    self.voice = voice
    self.image_generator = image_generator
    self.tts_provider = tts_provider

  def generate_video_content_from_idea(self, subject, idea_seed):
    content_package = MultimediaComposition(subject, self.audio_path, self.image_path)

    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)

    content_package.set_chosen_idea(ideas[idea_seed])
    video_transcript = self.text_processor.generate_transcript_from_idea(self.client, content_package.get_chosen_idea())
    content_package.set_transcript(video_transcript)

    # Run audio generation and image generation concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
      # Start audio generation
      audio_future = executor.submit(
        self.audio_processor.generate_audio_from_text, 
        content_package.get_transcript_string(), 
        self.audio_path + "/audio.mp3", 
        self.voice,
        self.tts_provider
      )
      
      # Start image generation in parallel
      image_future = executor.submit(
        self.image_processor.generate_images,
        content_package.get_transcript_array(),
        content_package.get_chosen_idea(),
        self.image_path
      )
      
      # Wait for audio to complete since we need it for subtitles
      audio_future.result()
      
      # Generate subtitles now that audio is ready
      subtitles = self.subtitle_processor.generate_subtitles(self.audio_path + "/audio.mp3")
      content_package.set_subtitles(subtitles.words)
      
      # Make sure image generation is complete before returning
      image_future.result()
    
    print("Video content generation completed successfully")
    return content_package

  def batch_video_generate(self, subject, num_videos):
    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)
    video_clips = []
    if num_videos > len(ideas):
      raise ValueError("Number of videos requested is greater than the number of ideas available. Please choose 9 or fewer videos to generate at once.")

    # Create directories for all videos upfront
    for i in range(min(num_videos, len(ideas))):
      os.makedirs(f"{self.audio_path}/{i}", exist_ok=True)
      os.makedirs(f"{self.image_path}/{i}", exist_ok=True)

    # Use ThreadPoolExecutor to process multiple videos concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(num_videos, 3)) as executor:
      # Submit all video generation tasks
      future_to_index = {
        executor.submit(self._generate_single_video, subject, ideas[i], i): i
        for i in range(min(num_videos, len(ideas)))
      }
      
      # Process results as they complete
      for future in concurrent.futures.as_completed(future_to_index.keys()):
        index = future_to_index[future]
        try:
          video_clip = future.result()
          video_clips.append(video_clip)
          print(f"Video {index} completed successfully")
        except Exception as e:
          print(f"Video {index} generation failed: {e}")
    
    return video_clips

  def _generate_single_video(self, subject, idea, index):
    """Helper method to generate a single video for batch processing"""
    video_clip = MultimediaComposition(subject, f"{self.audio_path}/{index}", f"{self.image_path}/{index}")
    
    video_clip.set_chosen_idea(idea)
    video_transcript = self.text_processor.generate_transcript_from_idea(self.client, video_clip.get_chosen_idea())
    video_clip.set_transcript(video_transcript)

    # Run audio and image generation concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
      audio_future = executor.submit(
        self.audio_processor.generate_audio_from_text, 
        video_clip.get_transcript_string(), 
        f"{self.audio_path}/{index}/audio.mp3", 
        self.voice,
        self.tts_provider
      )
      
      image_future = executor.submit(
        self.image_processor.generate_images,
        video_clip.get_transcript_array(),
        video_clip.get_chosen_idea(),
        f"{self.image_path}/{index}"
      )
      
      # Wait for audio to complete first
      audio_future.result()
      
      # Generate subtitles
      subtitles = self.subtitle_processor.generate_subtitles(f"{self.audio_path}/{index}/audio.mp3")
      video_clip.set_subtitles(subtitles.words)
      
      # Make sure image generation is complete
      image_future.result()
    
    return video_clip

  def generate_content_from_transcript(self, transcript):
    pass

  def generate_content_from_article(self, article_link):
    pass

  def generate_shorts_content_from_youtube_video(self, youtube_link):
    pass

  def generate_title_from_subtitles(self, subtitles):
    pass