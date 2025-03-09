from content_generation_workflow import ContentGenerationWorkflow
from video_editing_workflow import VideoEditingWorkflow
from models.editing_options import EditingOptions
from utils.utilities import save_object
import os

class VideoPipelineWorkflow:
    def __init__(self, 
                 # Content generation params
                 client,
                 image_path,
                 audio_path,
                 voice,
                 image_generator="openai",
                 tts_provider="openai",
                 # Video editing params
                 editing_options=None):
        self.content_generation_workflow = ContentGenerationWorkflow(
            client, 
            image_path, 
            audio_path, 
            voice, 
            image_generator,
            tts_provider
        )
        self.editing_options = editing_options if editing_options else EditingOptions()
        self.output_path = os.path.dirname(image_path)
        self.video_clip_path = self.output_path + "/video_clip"
        
        if not os.path.exists(self.video_clip_path):
            os.makedirs(self.video_clip_path, exist_ok=True)
    
    def generate_complete_video(self, subject, idea_seed):
        """Generate content and create a complete video in one step"""
        # Generate the content
        print("Generating content...")
        content_package = self.content_generation_workflow.generate_video_content_from_idea(subject, idea_seed)
        
        # Save the content package
        save_object(content_package, "video_clip", self.video_clip_path)
        print(f"Content saved to {self.video_clip_path}/video_clip.pkl")
        
        # Initialize the video editing workflow
        video_editing_workflow = VideoEditingWorkflow(content_package, self.output_path, self.editing_options)
        
        # Generate the video
        print("Editing video...")
        video_editing_workflow.generate_video_from_content()
        
        print(f"Video generation completed. Final video saved to {self.output_path}/output.mp4")
        return self.output_path + "/output.mp4"
    
    def batch_generate_videos(self, subject, num_videos, editing_options=None):
        """Generate multiple videos on the same subject in batch mode"""
        if not editing_options:
            editing_options = self.editing_options
        
        final_videos = []
        
        # Generate all content
        print(f"Generating {num_videos} videos for subject: {subject}")
        video_clips = self.content_generation_workflow.batch_video_generate(subject, num_videos)
        
        # Process each generated content
        for i, content_package in enumerate(video_clips):
            # Save the content package
            save_object(content_package, f"video_clip_{i}", self.video_clip_path)
            
            # Create video output subdirectory
            video_output_path = f"{self.output_path}/video_{i}"
            os.makedirs(video_output_path, exist_ok=True)
            
            # Initialize the video editing workflow
            video_editing_workflow = VideoEditingWorkflow(content_package, video_output_path, editing_options)
            
            # Generate the video
            print(f"Editing video {i+1}/{len(video_clips)}...")
            video_editing_workflow.generate_video_from_content()
            
            final_videos.append(f"{video_output_path}/output.mp4")
        
        print(f"Batch video generation completed. {len(final_videos)} videos saved.")
        return final_videos