class MultimediaComposition:

    def __init__(self, name, audio_file_path, image_file_paths):
      self.name = name
      self.transcript_array = []
      self.transcript_string = ""
      self.ideas = []
      self.audio_file_path = audio_file_path
      self.image_file_paths = image_file_paths
      self.chosen_idea = ""
      self.subtitles = ""

    def set_transcript(self, transcript_array):
      self.transcript_array = transcript_array
      self.transcript_string = " ".join(transcript_array)

    def set_chosen_idea(self, chosen_idea):
      self.chosen_idea = chosen_idea

    def set_subtitles(self, subtitles):
      self.subtitles = subtitles
    
    def get_chosen_idea(self):
      return self.chosen_idea
  
    def get_transcript_string(self):
      return self.transcript_string

    def get_transcript_array(self):
      return self.transcript_array