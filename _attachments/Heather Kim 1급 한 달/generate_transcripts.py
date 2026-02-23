import whisper
import json
import os
import sys

audio_filename = None

# 1️⃣ CLI 인자가 있으면 그걸 우선 사용
if len(sys.argv) > 1:
    audio_filename = sys.argv[1]
    print(f"Using CLI argument: {audio_filename}")

# 2️⃣ 인자가 없으면 tkinter 파일 선택창 사용
if not audio_filename:
    try:
        import tkinter as tk
        from tkinter.filedialog import askopenfilename

        root = tk.Tk()
        root.withdraw()
        audio_filename = askopenfilename()

        if not audio_filename:
            print("파일 선택이 취소되었습니다.")
            sys.exit(1)

        print(f"You selected: {audio_filename}")

    except Exception:
        print("파일 경로를 인자로 넘기거나 tkinter를 설치하세요.")
        sys.exit(1)

# 파일 존재 확인
if not os.path.exists(audio_filename):
    print(f"파일을 찾을 수 없습니다: {audio_filename}")
    sys.exit(1)

# -------------------------------
# Whisper 설정
# -------------------------------

model_name = "small"
start: float = None
end: float = None

print("Loading audio...")
audio = whisper.load_audio(audio_filename)
SAMPLE_RATE = 16000

if end is not None:
    audio = audio[:int(end * SAMPLE_RATE)]
if start is not None:
    audio = audio[int(start * SAMPLE_RATE):]

print(f"Loading Whisper model '{model_name}'...")
model = whisper.load_model(model_name)

print("Transcribing...")
result = model.transcribe(audio, verbose=False)

# 세그먼트 정리
for segment in result.get("segments", []):
    for k in ["id", "seek", "tokens", "temperature", "avg_logprob", "compression_ratio", "no_speech_prob"]:
        segment.pop(k, None)

    if start is not None:
        if "start" in segment:
            segment["start"] += start
        if "end" in segment:
            segment["end"] += start

# JSON 저장
base, _ext = os.path.splitext(audio_filename)
output_filename = base + ".json"

with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved transcript: {output_filename}")
print("Done!")
