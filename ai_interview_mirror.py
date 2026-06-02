import time
import cv2
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

print("=== AI INTERVIEW MIRROR ===")

print("\nChoose Interview Type")
print("1. HR")
print("2. Java")
print("3. Python")
print("4. DBMS")
print("5. Operating System")

choice = input("Enter choice (1-5): ")

if choice == "1":
    questions = [
        "Tell me about yourself",
        "What are your strengths",
        "What are your weaknesses",
        "Why should we hire you",
        "Where do you see yourself in five years"
    ]

elif choice == "2":
    questions = [
        "What is Java",
        "What is OOP",
        "What is inheritance",
        "Difference between method overloading and overriding",
        "What is polymorphism"
    ]

elif choice == "3":
    questions = [
        "What is Python",
        "Difference between list and tuple",
        "What is a function",
        "What are Python libraries",
        "What is exception handling"
    ]

elif choice == "4":
    questions = [
        "What is DBMS",
        "What is normalization",
        "Difference between SQL and NoSQL",
        "What is a primary key",
        "What is a join"
    ]

elif choice == "5":
    questions = [
        "What is a process",
        "Difference between process and thread",
        "What is deadlock",
        "What is CPU scheduling",
        "What is semaphore"
    ]

else:
    print("Invalid choice. Defaulting to HR.")
    questions = [
        "Tell me about yourself",
        "What are your strengths",
        "What are your weaknesses",
        "Why should we hire you",
        "Where do you see yourself in five years"
    ]

# Filler words
filler_words = [
    "umm", "um", "uh", "ah", "like",
    "actually", "basically", "okay",
    "so", "well", "honestly", "just"
]

filler_phrases = [
    "i think",
    "you know",
    "kind of",
    "sort of",
    "to be honest",
    "i mean"
]

recognizer = sr.Recognizer()

fs = 44100
record_seconds = 20

total_score = 0
total_fillers = 0
eye_scores = []

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

for q in questions:

    print("\n=================================")
    print("Question:", q)
    print("Speak your answer (20 seconds)...")

    start_time = time.time()

    # ----------------------------
    # Record Voice
    # ----------------------------
    recording = sd.rec(
        int(record_seconds * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    end_time = time.time()
    response_time = end_time - start_time

    wav.write("voice.wav", fs, recording)

    # ----------------------------
    # Speech to text
    # ----------------------------
    try:
        with sr.AudioFile("voice.wav") as source:
            audio = recognizer.record(source)

        answer = recognizer.recognize_google(audio)
        answer = answer.lower()

        print("You said:", answer)

    except Exception:
        answer = ""
        print("Could not understand audio.")

    # ----------------------------
    # Filler Detection
    # ----------------------------
    filler_count = 0
    detected_fillers = []

    words = answer.split()

    for word in words:
        if word in filler_words:
            filler_count += 1
            detected_fillers.append(word)

    for phrase in filler_phrases:
        if phrase in answer:
            filler_count += 1
            detected_fillers.append(phrase)

    long_pause = False

    if response_time > 20:
        long_pause = True
        filler_count += 1

    # ----------------------------
    # Eye Contact Check
    # ----------------------------
    print("\nChecking eye contact...")

    cap = cv2.VideoCapture(0)

    eye_start = time.time()
    face_count = 0
    total_frames = 0

    while True:

        success, img = cap.read()

        if not success:
            break

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            1.1,
            5
        )

        total_frames += 1

        if len(faces) > 0:
            face_count += 1

            for (x, y, w, h) in faces:
                cv2.rectangle(
                    img,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    2
                )

        cv2.imshow(
            "Eye Contact Check",
            img
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if time.time() - eye_start > 5:
            break

    cap.release()
    cv2.destroyAllWindows()

    eye_score = (
        face_count / total_frames
    ) * 100

    eye_scores.append(eye_score)

    # ----------------------------
    # Communication Score
    # ----------------------------
    score = 100 - (filler_count * 5)

    if score < 50:
        score = 50

    total_score += score
    total_fillers += filler_count

    # ----------------------------
    # Feedback
    # ----------------------------
    print("\n===== FEEDBACK =====")
    print("Detected fillers:",
          detected_fillers)

    print("Filler count:",
          filler_count)

    if long_pause:
        print("Long pause detected")

    print("Communication Score:",
          score)

    print("Eye Contact Score:",
          round(eye_score, 2))

# =================================
# Final Report
# =================================
average_score = (
    total_score / len(questions)
)

average_eye = (
    sum(eye_scores) /
    len(eye_scores)
)

print("\n========== FINAL REPORT ==========")
print("Questions Answered:",
      len(questions))

print("Total Fillers:",
      total_fillers)

print("Average Communication Score:",
      round(average_score, 2))

print("Average Eye Contact Score:",
      round(average_eye, 2))

overall = (
    average_score +
    average_eye
) / 2

print("Overall Interview Score:",
      round(overall, 2))

if overall >= 85:
    performance = "Excellent"

elif overall >= 70:
    performance = "Good"

elif overall >= 50:
    performance = "Average"

else:
    performance = "Needs Improvement"

print("Performance:", performance)