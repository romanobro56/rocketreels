import unittest
import pickle
import argparse
from models.video_wrapper import VideoWrapper
from models.multimedia_composition import MultimediaComposition
from utils.utilities import get_audio_duration

TEST_VIDEO_PATH = None
TEST_VIDEO_CONTENT = "/test_video_content"

"""
IMPORTANT DISTINCTION:
the VideoClip class is for referencing the components of video editing comprising the finished product
the VideoWrapper class is for referencing the intrinsic properties of the final video which was made from the contents of VideoClip
Do not forget while writing tests 
"""

class TestVideoEditingMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_VIDEO_CONTENT + "/video_clip/video_clip.pkl", 'rb') as file:
          cls.video_content = pickle.load(file)
        cls.video_wrapper = VideoWrapper(TEST_VIDEO_PATH)
        if not isinstance(cls.video_content, MultimediaComposition):
          raise ValueError("Invalid video content. Please provide a valid video clip object for reference.")
        print(f"Loaded an instance of VideoClip with name: {cls.video_content.name}")

    def test_get_runtime(self):
      audio_path = TEST_VIDEO_CONTENT + "/audio/audio.mp3"
      audio_duration = get_audio_duration(audio_path)  
      expected_runtime = audio_duration  # Using audio duration as the expected runtime
      self.assertAlmostEqual(self.video_wrapper.get_runtime(), expected_runtime, places=2, msg="Runtime does not match expected value.")

    def test_get_aspect_ratio(self):
      expected_aspect_ratio = self.video_content.get_aspect_ratio()
      self.assertAlmostEqual(self.video_wrapper.get_aspect_ratio(), expected_aspect_ratio, places=2, msg="Aspect ratio does not match expected value.")

    def test_get_resolution(self):
      expected_horizontal_resolution, expected_vertical_resolution = self.video_content.get_resolution()
      self.assertEqual(self.video_wrapper.get_resolution(), (expected_horizontal_resolution, expected_vertical_resolution), msg="Resolution does not match expected value.")
    
    def test_get_frame_rate(self):
      expected_frame_rate = self.video_content.get_frame_rate()
      self.assertEqual(self.video_wrapper.get_frame_rate(), expected_frame_rate, msg="Frame rate does not match expected value.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run video editing tests.')
    parser.add_argument('--video-path', required=True, help='Path to the test video content.')
    
    # Parse only known arguments and leave the rest for unittest
    args, unittest_args = parser.parse_known_args()
    TEST_VIDEO_PATH = args.video_path

    # Run unittest with the remaining arguments
    unittest.main(argv=['first-arg-is-ignored'] + unittest_args)
