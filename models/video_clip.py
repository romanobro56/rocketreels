class VideoClip:
    def __init__(self, name, audio_file_path, image_file_paths, expected_frame_rate=60, expected_aspect_ratio=9/16, expected_horizontal_resolution=1080, expected_vertical_resolution=1920):
      self.name = name
      self.transcript_array = []
      self.transcript_string = ""
      self.ideas = []
      self.audio_file_path = audio_file_path
      self.image_file_paths = image_file_paths
      self.chosen_idea = ""
      self.subtitles = ""
      self.frame_rate = expected_frame_rate
      self.aspect_ratio = expected_aspect_ratio
      self.horizontal_resolution = expected_horizontal_resolution
      self.vertical_resolution = expected_vertical_resolution

    def set_transcript(self, transcript_array):
      self.transcript_array = transcript_array
      self.transcript_string = " ".join(transcript_array)

    def set_ideas(self, ideas):
      self.ideas = ideas

    def set_chosen_idea(self, chosen_idea):
      self.chosen_idea = chosen_idea

    def set_audio_file_path(self, audio_file_path):
      self.audio_file_path = audio_file_path
    
    def set_image_file_paths(self, image_file_paths):
      self.image_file_paths = image_file_paths

    def set_subtitles(self, subtitles):
      self.subtitles = subtitles

    def set_frame_rate(self, expected_frame_rate):
      self.frame_rate = expected_frame_rate

    def set_aspect_ratio(self, expected_aspect_ratio):
      self.expected_aspect_ratio = expected_aspect_ratio
    
    def set_resolution(self, expected_horizontal_resolution, expected_vertical_resolution):
      self.expected_horizontal_resolution = expected_horizontal_resolution
      self.expected_vertical_resolution = expected_vertical_resolution

    def get_transcript_array(self):
      return self.transcript_array
    
    def get_transcript_string(self):
      return self.transcript_string
    
    def get_ideas(self):
      return self.ideas
    
    def get_chosen_idea(self):
      return self.chosen_idea
    
    def get_audio_file_path(self):
      return self.audio_file_path
    
    def get_image_file_paths(self):
      return self.image_file_paths
    
    def get_subtitles(self):
      return self.subtitles
    
    def get_frame_rate(self):
      return self.frame_rate
    
    def get_aspect_ratio(self):
      return self.expected_aspect_ratio
        
    def get_resolution(self):
      return self.horizontal_resolution, self.vertical_resolution
    