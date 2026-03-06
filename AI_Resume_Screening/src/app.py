import os
from resume_parser import parse_resume
from text_preprocessing import preprocess
from matcher import calculate_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESUME_DIR = os.path.join(BASE_DIR, "resumes")
JD_PATH = os.path.join(BASE_DIR, "job_description", "jd.txt")

# Load Job Description
with open(JD_PATH, "r", encoding="utf-8") as f:
    jd_text = preprocess(f.read())

resume_texts = []
resume_names = []

for file in os.listdir(RESUME_DIR):
    file_path = os.path.join(RESUME_DIR, file)

    if file.endswith((".pdf", ".docx")):
        text = parse_resume(file_path)
        processed = preprocess(text)
        resume_texts.append(processed)
        resume_names.append(file)

scores = calculate_similarity(resume_texts, jd_text)

ranked = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)

print("\n======= AI RESUME SCREENING RESULTS =======\n")
for name, score in ranked:
    print(f"{name} --> Match Score: {round(score * 100, 2)}%")
