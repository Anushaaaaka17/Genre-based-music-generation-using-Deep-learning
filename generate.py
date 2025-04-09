from tensorflow.keras.models import load_model
import numpy as np
from music21 import stream, note, instrument
from data_loader import extract_notes, prepare_sequences
import os

def generate_music(genre, pitch_names, sequence_length=50):
    print(" Generating music for genre:", genre)

    # Load trained model
    model_path = f"weights/{genre}_model.h5"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    model = load_model(model_path)

    # Extract notes from the dataset
    notes = extract_notes(f"dataset/{genre}")

    # Mapping notes to integers and vice versa
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))
    int_to_note = dict((number, note) for number, note in enumerate(pitch_names))

    # Random starting point for generation
    if len(notes) <= sequence_length:
        raise ValueError("Not enough notes to generate music. Try with more training data.")
    
    start = np.random.randint(0, len(notes) - sequence_length)
    pattern = notes[start:start + sequence_length]
    input_seq = [note_to_int[n] for n in pattern]

    output_notes = []

    # Generate 100 notes
    for _ in range(100):
        input_data = np.reshape(input_seq, (1, sequence_length))
        prediction = model.predict(input_data, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        output_notes.append(result)
        input_seq.append(index)
        input_seq = input_seq[1:]

    # Convert to MIDI
    midi_stream = stream.Stream()
    midi_stream.append(instrument.Piano())
    for pitch in output_notes:
        try:
            n = note.Note(int(pitch))
            n.quarterLength = 0.5
            midi_stream.append(n)
        except:
            print(f" Skipped invalid pitch: {pitch}")

    # Save MIDI file
    if not os.path.exists("output"):
        os.makedirs("output")
    midi_stream.write('midi', fp=f"output/{genre}_output.mid")

    print("MIDI generation complete:", f"output/{genre}_output.mid")
