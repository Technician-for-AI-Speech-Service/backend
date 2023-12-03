from os import path
from pydub import AudioSegment

# files
src = "audio.mp3"
dst = "audio.wav"

# convert wav to mp3
audSeg = AudioSegment.from_mp3("audio.mp3")
audSeg.export(dst, format="wav")