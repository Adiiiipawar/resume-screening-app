import streamlit as st
import os
import pandas as pd
import plotly.express as px
from resume_parser import parse_resume
from ranker import rank_resumes
from utils import extract_keywords

RESUME_FOLDER = "resumes"
OUTPUT_FOLDER = "output"

# Create folders if not exist
os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("📄 AI-Powered Resume Screening Tool")
st.markdown("Upload resumes and paste a job description to rank candidates using NLP & cosine similarity.")

# --- Job Description Input ---
st.subheader("1️⃣ Paste Job Description")
job_description = st.text_area("Job Description", height=200)

# --- Resume Upload ---
st.subheader("2️⃣ Upload Resume PDFs")
uploaded_files = st.file_uploader("Upload multiple resumes", type=["pdf"], accept_multiple_files=True)

# --- Action Button ---
if st.button("🔍 Rank Resumes"):
    if not job_description or not uploaded_files:
        st.warning("Please upload resumes and enter a job description.")
    else:
        resume_texts = []
        resume_names = []

        for file in uploaded_files:
            file_path = os.path.join(RESUME_FOLDER, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            
            text = parse_resume(file_path)
            resume_texts.append(text)
            resume_names.append(file.name)

        # Rank resumes
        ranked = rank_resumes(job_description, resume_texts)

        # Extract keywords from job description
        jd_keywords = extract_keywords(job_description)

        # Build final results table
        final_results = []
        for i, (idx, score) in enumerate(ranked):
            text = resume_texts[idx].lower()
            matched_skills = [kw for kw in jd_keywords if kw in text]

            final_results.append({
                "Rank": i + 1,
                "Resume File": resume_names[idx],
                "Matching Score (%)": round(score * 100, 2),
                "Matched Skills": ', '.join(matched_skills),
                "Skill Match Count": len(matched_skills)
            })

        df = pd.DataFrame(final_results)
        df = df.sort_values(by="Matching Score (%)", ascending=False)

        st.success("Resumes ranked successfully!")
        st.dataframe(df, use_container_width=True)

        # 📊 Plotly chart for visual comparison
        st.subheader("📊 Visual Comparison of Resume Scores")
        fig = px.bar(
            df,
            x="Resume File",
            y="Matching Score (%)",
            color="Skill Match Count",
            text="Matching Score (%)",
            title="Resume Matching Score vs Candidate",
        )
        fig.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        # 📁 Export CSV
        output_path = os.path.join(OUTPUT_FOLDER, "ranked_resumes.csv")
        df.to_csv(output_path, index=False)
        st.download_button("⬇️ Download CSV", data=df.to_csv(index=False),
                           file_name="ranked_resumes.csv", mime="text/csv")

        # 📝 Optional: Export top 3 resumes summary
        top_3 = df.head(3)
        st.download_button("⬇️ Download Top 3 Summary", data=top_3.to_csv(index=False),
                           file_name="top_3_resumes.csv", mime="text/csv")
