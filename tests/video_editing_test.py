import unittest

class TestVideoEditingMethods(unittest.TestCase):
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

  