from train_model import train, get_input_shape_and_notes
from generate import generate_music
from converter import midi_to_mp3
from tensorflow.keras.models import load_model
import os

genres = ["classical", "retro", "party"]

print("Choose a genre:")
for i, g in enumerate(genres):
    print(f"{i+1}. {g.capitalize()}")

choice = int(input("Enter choice: ")) - 1
genre = genres[choice]

model_path = f"saved_models/{genre}_model.h5"

# Step 1: Load or Train model
if os.path.exists(model_path):
    print(" Pretrained model found. Loading...")
    model = load_model(model_path)
    pitch_names, input_shape = get_input_shape_and_notes(genre)
else:
    print(" Training new model...")
    pitch_names, model, input_shape = train(genre)

# Step 2: Generate music
generate_music(genre, pitch_names)



# Step 3: Convert generated MIDI to MP3
midi_path = f"output/{genre}_output.mid"
mp3_path = f"output/{genre}_output.mp3"
midi_to_mp3(midi_path, mp3_path) 

print(f" Music generated and saved: {mp3_path}")
