from video_editing_workflow import VideoEditingWorkflow
from models.editing_options import EditingOptions
import pickle
import os

content_path = os.getcwd() + "/video_ZpsDvANs_test"

def load_object(filename):
    with open(filename, 'rb') as inp:  # Read in binary mode
        return pickle.load(inp)

content_package = load_object("/Users/romanpisani/Desktop/Coding/AutoShorts/test_video_content/video_clip/video_clip.pkl")

editing_options = EditingOptions("vertical", "HD", 30)
video_editing_workflow = VideoEditingWorkflow(content_package, content_path, editing_options)



video_editing_workflow.generate_video_from_content()

