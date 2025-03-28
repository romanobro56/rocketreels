from utils.utilities import format_time

from PIL import ImageFont
import os

class SubtitleProcessor:
  def __init__(self, client=None):
    self.client = client

  def generate_subtitles(self, audio_path):
    audio_file = open(audio_path, "rb")

    transcript = self.client.audio.transcriptions.create(
      file=audio_file,
      model="whisper-1",
      response_format="verbose_json",
      timestamp_granularities=["word"]
    )

    return transcript
  
  def get_image_timestamps(self, subtitles, transcript_array):
    image_timestamps = []
    sentence_lengths = [len(sentence.split(" ")) for sentence in transcript_array]

    word_index = 0

    for sentence_length in sentence_lengths:
        word_count = 0
        start_index = word_index
        while word_count < sentence_length and word_index < len(subtitles):
            word_count += 1
            word_index += 1
        
        # Check if we're dealing with TranscriptionWord objects or dictionaries
        if start_index < len(subtitles):
            if hasattr(subtitles[start_index], 'start'):
                # TranscriptionWord object case - use attribute access
                start_time = subtitles[start_index].start if start_index < len(subtitles) else 0
                end_time = subtitles[word_index - 1].end if word_index - 1 < len(subtitles) else subtitles[-1].end
            else:
                # Dictionary case - use key access
                start_time = subtitles[start_index]["start"] if start_index < len(subtitles) else 0
                end_time = subtitles[word_index - 1]["end"] if word_index - 1 < len(subtitles) else subtitles[-1]["end"]
        else:
            # Default fallback if start_index is out of bounds
            start_time = 0
            end_time = 0
            if len(subtitles) > 0:
                if hasattr(subtitles[-1], 'end'):
                    end_time = subtitles[-1].end
                else:
                    end_time = subtitles[-1]["end"]
                    
        image_timestamps.append({"start": start_time, "end": end_time})

    return image_timestamps
       

  def set_sub_granularity_json(self, subtitle_words, editing_options):
    text_width = editing_options.get_subtitle_granularity_width()
    font = ImageFont.truetype("/Users/romanpisani/Desktop/Coding/AutoShorts/TitanOne-Regular.ttf", size=editing_options.get_font_size())
    new_subtitles = []
    running_line_width = 0
    start_time = None
    current_line = []
    
    for subtitle in subtitle_words:
        # Check if subtitle is a TranscriptionWord object or a dictionary
        if hasattr(subtitle, 'word'):
            word = subtitle.word
            start = subtitle.start
            end = subtitle.end
        else:
            word = subtitle["word"]
            start = subtitle["start"]
            end = subtitle["end"]
            
        width = font.getlength(word + " ")

        if start_time is None:
            start_time = start

        if running_line_width + width > text_width * editing_options.get_horizontal_resolution():
            new_subtitles.append({
                "text": " ".join(current_line),
                "start": start_time,
                "end": end
            })
            current_line = [word]
            running_line_width = width
            start_time = start
        else:
            current_line.append(word)
            running_line_width += width

    if current_line:
        # For the last subtitle, get the end time properly
        last_end = 0
        if subtitle_words:
            if hasattr(subtitle_words[-1], 'end'):
                last_end = subtitle_words[-1].end
            else:
                last_end = subtitle_words[-1]["end"]
                
        new_subtitles.append({
            "text": " ".join(current_line),
            "start": start_time,
            "end": last_end
        })

    return new_subtitles
  
  def json_to_srt(self, json_obj):
    srt_content = ""
    for index, subtitle in enumerate(json_obj, start=1):
        start_time = format_time(subtitle['start'])
        
        if index < len(json_obj):
            end_time = format_time(json_obj[index]['start'])
        else:
            end_time = format_time(subtitle['end'])
        
        srt_content += f"{index}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{subtitle['text']}\n\n"
    
    return srt_content.strip()