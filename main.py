import numpy as np
import sounddevice as sd
import wave
from faster_whisper import WhisperModel
import ollama
import subprocess

def speak(text):
    p = subprocess.Popen(["espeak-ng", "-v", "ru+f5","-s","100","-p","40", text])
    p.wait()  

# === Whisper ===
model_size = "large-v3"
whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")

CHUNK = 1024
RATE = 16000
FORMAT = np.int16
CHANNELS = 1
RECORD_SECONDS = 5

messages = []

def record_fixed_time(filename="audio.wav", record_seconds=RECORD_SECONDS):
    print(f"[🎙] Запись {record_seconds} секунд...")
    frames = []

    def callback(indata, frames_count, time_info, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=FORMAT, blocksize=CHUNK, callback=callback):
        sd.sleep(record_seconds * 1000)

    print("[✅] Запись завершена.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(FORMAT).itemsize)
        wf.setframerate(RATE)
        wf.writeframes(np.concatenate(frames).tobytes())

    return filename

def transcribe(filename):
    segments, info = whisper_model.transcribe(filename, beam_size=8)
    print(f"[🧠] Язык: {info.language}, вероятность: {info.language_probability:.2f}")
    text = ''.join(segment.text for segment in segments)
    return text

def main():
    while True:
        audio_path = record_fixed_time("audio.wav")
        user_text = transcribe(audio_path)

        if not user_text.strip():
            print("[🔇] Ничего не сказано или ошибка.")
            continue

        print("[🗣] Пользователь:", user_text)
        messages.append({"role": "user", "content": user_text})

        response = ollama.chat('qwen2.5-coder:latest', messages=messages)
        assistant_text = response['message']['content']
        print("[🤖] Ассистент:", assistant_text)

        messages.append({"role": "assistant", "content": assistant_text})

        speak(assistant_text)

if __name__ == "__main__":
    main()