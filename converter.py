from pydub import AudioSegment
import subprocess
import os
AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"

def midi_to_mp3(midi_file, mp3_file):
    subprocess.run(['fluidsynth', '-ni', 'soundfont.sf2', midi_file, '-F', 'temp.wav', '-r', '44100'])
    sound = AudioSegment.from_wav("temp.wav")
    sound.export(mp3_file, format="mp3")
    os.remove("temp.wav")
