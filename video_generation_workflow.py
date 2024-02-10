from generation.text_processing import TextProcessor
from generation.audio_processing import AudioProcessor
from generation.image_processing import ImageProcessor
from editing.subtitle_processing import SubtitleProcessor
from editing.video_processing import VideoProcessor
from models.video_clip import VideoClip

class VideoGenerationWorkflow:
  def __init__(self, client, output_path):
    self.text_processor = TextProcessor(client)
    self.audio_processor = AudioProcessor(client)
    self.image_processor = ImageProcessor(client)
    self.subtitle_processor = SubtitleProcessor(client)
    self.video_processor = VideoProcessor()
    self.output_path = output_path
    self.client = client

  async def generate_video_from_idea(self, subject, idea_seed):
    video_clip = VideoClip()

    ideas = self.text_processor.generate_ideas_from_subject(self.client, subject)
    video_clip.set_chosen_idea(ideas[idea_seed])

    video_clip.set_transcript(self.text_processor.generate_transcript_from_idea(self.client, video_clip.getIdea()))

    self.audio_processor.generate_audio_from_text(video_clip.transcript_string(), self.output_path + "/audio.mp3")

  async def batch_video_generate(self, subject):
    pass

  async def generate_video_from_transcript(self, transcript):
    pass

  async def generate_video_from_article(self, article_link):
    pass