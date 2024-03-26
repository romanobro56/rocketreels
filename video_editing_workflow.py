from editing.subtitle_processing import SubtitleProcessor
from editing.video_processing import VideoProcessor

class VideoEditingWorflow:
  def __init__(self, content_directory, content_package):
    self.content_directory = content_directory
    self.content_package = content_package
    self.video_processor = VideoProcessor()
    self.subtitle_processor = SubtitleProcessor()