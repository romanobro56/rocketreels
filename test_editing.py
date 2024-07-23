from models.multimedia_composition import MultimediaComposition
from video_editing_workflow import VideoEditingWorkflow
from models.editing_options import EditingOptions
from utils.utilities import load_object
import pickle
import os

content_file = input("type the name of the directory in the output folder that you want to test in: ")
content_path = os.getcwd() + "/output/" + content_file


content_package = load_object( content_path + "/video_clip/video_clip.pkl")
if type(content_package) != MultimediaComposition:
    raise TypeError("Content package is of type" + str(type(content_package)) + ", expected type " + str(MultimediaComposition) + ". If these look the same you may have edited the multimedia composition class then tried to load an older object")

editing_options = EditingOptions("vertical", "HD", 30, font_size="extra_large", font_stroke_width=4,font_stroke_color="black")
video_editing_workflow = VideoEditingWorkflow(content_package, content_path, editing_options)

video_editing_workflow.generate_video_from_content()