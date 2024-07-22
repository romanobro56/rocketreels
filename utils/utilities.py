from pydub import AudioSegment
import pickle

def save_object(obj, name, path):
    with open(f'{path}/{name}.pkl', 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

            
# Function to load and deserialize the object from a file
def load_object(filename):
    with open(filename, 'rb') as inp: 
        return pickle.load(inp)
    

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')

  
def get_audio_duration(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    duration_milliseconds = len(audio)
    duration_seconds = duration_milliseconds / 1000.0

    return duration_seconds


def write_string_to_file(string, file_path):
    with open(file_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(string)
