class VideoClip:
    def __init__(self, audio_file_path, image_file_paths):
        self.transcript_array = []
        self.transcript_string = ""
        self.ideas = []
        self.audio_file_path = audio_file_path
        self.image_file_paths = image_file_paths
        self.chosen_idea = ""

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

    def transcript_array(self):
      return self.transcript_array
    
    def transcript_string(self):
      return self.transcript_string
    
    def ideas(self):
      return self.ideas
    
    def chosen_idea(self):
      return self.chosen_idea
    
    def audio_file_path(self):
      return self.audio_file_path
    
    def image_file_paths(self):
      return self.image_file_paths
    