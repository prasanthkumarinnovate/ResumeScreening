import streamlit as st
import tempfile
import os

from resume_parser import parse_resume
from text_preprocessing import preprocess
from matcher import calculate_similarity

st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="centered")

# --------- Custom CSS ---------

st.markdown("""
<style>
/* Hide Streamlit top header bar */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Remove extra top spacing */
.block-container {
    padding-top: 1rem;
}

/* Import Professional Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* Background Image */
.stApp {
    background-image: url("https://images.pexels.com/photos/1367192/pexels-photo-1367192.jpeg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Dark overlay for readability */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 1%;
    height: 1%;
    background: rgba(20,20,20,0.65);
    backdrop-filter: blur(15px);
    z-index: -1;
}

/* Title */
h1 {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0px 3px 10px rgba(0,0,0,0.8);
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #e5e7eb;
    font-size: 18px;
    font-weight: 400;
    margin-bottom: 25px;
    text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
}

/* Upload title */
h3 {
    color: #ffffff;
    font-weight: 600;
    text-shadow: 0px 3px 10px rgba(0,0,0,0.8);
}

/* Glass File Upload Box */
[data-testid="stFileUploader"] {
    background: rgba(20,20,20,0.65);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-size: 18px;
    font-weight: 600;
    border-radius: 12px;
    height: 52px;
    border: none;
    box-shadow: 0px 4px 15px rgba(0,114,255,0.5);
    text-shadow: 0px 3px 10px rgba(0,0,0,0.8);
}

.stButton>button:hover {
    transform: scale(1.05);
    transition: 0.2s;
}

/* Result cards */
.result-card {
    background: rgba(20,20,20,0.65);
    backdrop-filter: blur(12px);
    padding: 18px;
    border-radius: 14px;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 5px 20px rgba(0,0,0,0.5);
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# --------- Header ---------

st.markdown("<h1 style='text-align:center'>📄 AI Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Upload Job Description and Resumes to find the best candidates</p>", unsafe_allow_html=True)

st.divider()

# --------- Upload Section ---------

st.subheader("📂 Upload Files")

# Job Description Upload
jd_file = st.file_uploader(
    "Upload Job Description (TXT / PDF / DOCX)",
    type=["txt", "pdf", "docx"]
)

# Resume Upload
resume_files = st.file_uploader(
    "Upload Resumes (PDF / DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

st.divider()

# --------- Analyze Button ---------

if st.button("🚀 Analyze Resumes", use_container_width=True):

    if jd_file is None or resume_files is None:
        st.error("⚠ Please upload Job Description and Resumes")

    else:

        with st.spinner("Analyzing resumes..."):

            # --------- Process Job Description ---------

            jd_extension = os.path.splitext(jd_file.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=jd_extension) as tmp:
                tmp.write(jd_file.read())
                jd_path = tmp.name

            if jd_extension == ".txt":
                with open(jd_path, "r", encoding="utf-8") as f:
                    jd_text = f.read()
            else:
                jd_text = parse_resume(jd_path)

            jd_processed = preprocess(jd_text)

            os.remove(jd_path)

            # --------- Process Resumes ---------

            resume_texts = []
            resume_names = []

            for resume in resume_files:

                extension = os.path.splitext(resume.name)[1]

                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
                    tmp.write(resume.read())
                    tmp_path = tmp.name

                text = parse_resume(tmp_path)
                processed = preprocess(text)

                resume_texts.append(processed)
                resume_names.append(resume.name)

                os.remove(tmp_path)

            # --------- Calculate Similarity ---------

            scores = calculate_similarity(resume_texts, jd_processed)

        st.success("✅ Analysis Completed")

        # --------- Display Results ---------

        st.subheader("📊 Resume Match Results")

        results = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)

        for name, score in results:

            percent = round(score * 100, 2)

            st.markdown(f"""
            <div class="result-card">
            <b>{name}</b><br>
            Match Score: <b>{percent}%</b>
            </div>
            """, unsafe_allow_html=True)

            st.progress(score)

        # --------- Top Candidate ---------

        top = results[0]

        st.success(f"🏆 Top Candidate: {top[0]} ({round(top[1]*100,2)}%)")