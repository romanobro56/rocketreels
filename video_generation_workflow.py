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
    video_clip = VideoClip(subject, self.audio_path, self.image_path)

    ideas =  self.text_processor.generate_ideas_from_subject(self.client, subject)
    video_clip.set_chosen_idea(ideas[idea_seed])
    video_transcript = self.text_processor.generate_transcript_from_idea(self.client, video_clip.get_chosen_idea())
    video_clip.set_transcript(video_transcript)
    print(video_clip.get_transcript_string())
    self.audio_processor.generate_audio_from_text(video_clip.get_transcript_string(), self.audio_path + "/audio.mp3", self.voice)
    subtitles = self.subtitle_processor.generate_subtitles(self.audio_path + "/audio.mp3")
    print(subtitles)
    video_clip.set_subtitles(subtitles)

    self.image_processor.generate_images(video_clip.get_transcript_array(), video_clip.get_chosen_idea(), self.image_path)
    print("images generated")
    return video_clip

  def edit_video_from_content(self, video_clip, input_path, output_path):
    self.video_processor.generate_video_from_clip(video_clip, self.output_path + "/video.mp4")
    pass


  def batch_video_generate(self, subject):
    video_clip = VideoClip()
    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)
    video_clip.set_ideas(ideas)

    for i, idea in enumerate(video_clip.get_ideas()):
      self.audio_processor.generate_audio_from_text(idea, self.output_path + f'/audio{i}.mp3', self.voice)


  def generate_content_from_transcript(self, transcript):
    pass

  def generate_content_from_article(self, article_link):
    pass

  def generate_shorts_content_from_youtube_video(self, youtube_link):
    pass

  def generate_title_from_subtitles(self, subtitles):
    pass