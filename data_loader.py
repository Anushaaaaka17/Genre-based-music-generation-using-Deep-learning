import pretty_midi
import os
import numpy as np

def extract_notes(folder_path):
    notes = []
    for file in os.listdir(folder_path):
        if file.endswith(".mid") or file.endswith(".midi"):
            midi = pretty_midi.PrettyMIDI(os.path.join(folder_path, file))
            for instrument in midi.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        notes.append(note.pitch)
    return notes

def prepare_sequences(notes, sequence_length=50):
    pitch_names = sorted(set(notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))
    
    network_input = []
    network_output = []
    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[note] for note in sequence_in])
        network_output.append(note_to_int[sequence_out])
        
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length))
    network_output = np.eye(len(pitch_names))[network_output]
    return network_input, network_output, len(pitch_names), pitch_names
