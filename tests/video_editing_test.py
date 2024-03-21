import unittest
import pickle
# unpickles video clip object and uses example video file to simulate video editing
from models.video_clip import VideoClip

class TestVideoEditingMethods(unittest.TestCase):

  def load_object(filename):
    with open(filename, 'rb') as inp:  # Read in binary mode
        return pickle.load(inp)
    
  def setUp(self, video_clip_path, output_path):
    self.video_clip = load_object(video_clip_path + "/video_clip.pkl")
    self.output_video = Video(output_path + "/video.mp4")

  def test_video_transcript(self):
    self.assertEqual(video_clip.get_transcript_string(), output_video.transcript())
    
  def test_video_length(self):
    self.assertEqual(video_clip.length_of_videos(), output_video.runtime())

  def test_video_subtitles(self):
    subtitles_length_difference = video_clip.subtitles_length() - output_video.subtitles_length()
    self.assertEqual( subtitles_length_difference > -10 and subtitles_length_difference < 10)

  def test_video_audio_levels(self):
    # checks if the audio is within an acceptable range
    pass

  def test_video_above_one_minute(self):
    self.assertEqual(video_clip.length_of_videos > 60)

  