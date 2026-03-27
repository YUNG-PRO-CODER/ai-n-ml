import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recording.wav"
TEXT_OUTPUT_FILENAME = "transcription.txt"

audio = pyaudio.PyAudio()

print("🎤 Recording... Speak now!")

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("✅ Recording finished.")

stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"💾 Saved audio as {WAVE_OUTPUT_FILENAME}")

recognizer = sr.Recognizer()

with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
    audio_data = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio_data)
    print("🧾 Transcription:", text)

    with open(TEXT_OUTPUT_FILENAME, "w") as f:
        f.write(text)

    print(f"💾 Saved transcription as {TEXT_OUTPUT_FILENAME}")

except sr.UnknownValueError:
    print("❌ Could not understand audio")
    text = ""
except sr.RequestError:
    print("❌ API unavailable")
    text = ""

audio_signal = np.frombuffer(b''.join(frames), dtype=np.int16)

plt.figure(figsize=(10, 4))
plt.plot(audio_signal)
plt.title("Audio Waveform")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.show()