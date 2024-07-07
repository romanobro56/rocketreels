from pydub import AudioSegment
import pickle

def save_object(obj, name, path):
    with open(path + "/${name}.pkl", 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
            

# Function to load and deserialize the object from a file
def load_object(filename):
    with open(filename, 'rb') as inp: 
        return pickle.load(inp)