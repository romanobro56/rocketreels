from generation.text_processing import TextProcessing
from generation.audio_processing import AudioProcessing
from generation.image_processing import ImageProcessing
from editing.subtitle_processing import SubtitleProcessing
from editing.video_processing import VideoProcessing
from models.video_clip import VideoClip

class VideoGenerationWorkflow:
  def __init__(self, client):
    self.video_clip = VideoClip()
    self.text_processor = TextProcessing()
    self.audio_processor = AudioProcessing()
    self.image_processor = ImageProcessing()
    self.subtitle_processor = SubtitleProcessing()
    self.video_processor = VideoProcessing()
    self.client = client

  async def generate_video_from_idea(self, subject, idea_seed):
      ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)
      self.video_clip.set_chosen_idea(ideas[idea_seed])

      transcript_array = self.text_processor.generate_transcript_from_idea(self.client, self.video_clip.getIdea())

  async def batch_video_generate(self, subject):
    pass

  async def generate_video_from_transcript(self, transcript):
    pass

  async def generate_video_from_article(self, article_link):
    pass