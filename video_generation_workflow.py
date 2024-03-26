from editing.subtitle_processing import SubtitleProcessor
from generation.image_processing import ImageProcessor
from generation.audio_processing import AudioProcessor
from generation.text_processing import TextProcessor
from editing.video_processing import VideoProcessor
from models.video_clip import VideoClip

import asyncio

class VideoGenerationWorkflow:
  def __init__(self, client, image_path, audio_path, voice):
    self.subtitle_processor = SubtitleProcessor(client)
    self.audio_processor = AudioProcessor(client)
    self.image_processor = ImageProcessor(client)
    self.text_processor = TextProcessor(client)
    self.video_processor = VideoProcessor()
    self.image_path = image_path
    self.audio_path = audio_path
    self.client = client
    self.voice = voice

  def generate_video_content_from_idea(self, subject, idea_seed):
    video_clip = VideoClip(subject, self.audio_path, self.image_path, "vertical", "SD", 30)

    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)

    video_clip.set_chosen_idea(ideas[idea_seed])
    video_transcript = self.text_processor.generate_transcript_from_idea(self.client, video_clip.get_chosen_idea())
    video_clip.set_transcript(video_transcript)

    self.audio_processor.generate_audio_from_text(video_clip.get_transcript_string(), self.audio_path + "/audio.mp3", self.voice)
    subtitles = self.subtitle_processor.generate_subtitles(self.audio_path + "/audio.mp3")

    video_clip.set_subtitles(subtitles)

    self.image_processor.generate_images(video_clip.get_transcript_array(), video_clip.get_chosen_idea(), self.image_path)
    print("video content done generating")
    return video_clip


  def batch_video_generate(self, subject):
    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)
    video_clips = []

    for i, idea in enumerate(ideas):
      video_clip = VideoClip(subject, self.audio_path, self.image_path, "vertical", "SD", 30)

      video_clip.set_chosen_idea(idea)
      video_transcript = self.text_processor.generate_transcript_from_idea(self.client, video_clip.get_chosen_idea())
      video_clip.set_transcript(video_transcript)

      self.audio_processor.generate_audio_from_text(video_clip.get_transcript_string(), self.audio_path + f"/{i}/audio.mp3", self.voice)
      subtitles = self.subtitle_processor.generate_subtitles(self.audio_path + f"/{i}/audio.mp3")

      video_clip.set_subtitles(subtitles)

      self.image_processor.generate_images(video_clip.get_transcript_array(), video_clip.get_chosen_idea(), self.image_path + f"/{i}")
      video_clips.append(video_clip)


  def generate_content_from_transcript(self, transcript):
    pass

  def generate_content_from_article(self, article_link):
    pass

  def generate_shorts_content_from_youtube_video(self, youtube_link):
    pass

  def generate_title_from_subtitles(self, subtitles):
    pass