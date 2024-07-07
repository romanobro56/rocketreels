from editing.subtitle_processing import SubtitleProcessor
from editing.video_processing import VideoProcessor

class VideoEditingWorkflow:
  def __init__(self, content_package, video_file_path, editing_options):
    # content package is an instance of MultimediaComposition which contains the content and file paths
    self.content_package = content_package
    self.video_processor = VideoProcessor(editing_options)
    self.subtitle_processor = SubtitleProcessor()
    self.video_file_path = video_file_path

  def generate_video_from_content(self):
    self.video_processor.generate_video_from_images(self.content_package, self.video_file_path)
    # self.subtitle_processor.overlay_subtitles(self.content_package, self.video_file_path)

    # self.video_processor.apply_effect(self.content_package, self.video_file_path, editing_options)
