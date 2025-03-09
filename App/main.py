import streamlit as st              # Import Streamlit for building the web app
from utils import extract_text_from_pdf  # Import PDF text extraction function from utils
from parser import parse_text       # Import text parsing function from parser
from matcher import calculate_match  # Import match calculation function from matcher
from analyzer import generate_suggestions  # Import suggestions generator from analyzer
import json                         # Import json module for JSON handling

st.title("Resume Analyzer with Gemini AI")  # Set the title of the Streamlit app

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")  # Create file uploader for resume PDF
job_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")  # Create file uploader for job description PDF

if resume_file and job_file:        # Check if both files are uploaded
    resume_text = extract_text_from_pdf(resume_file)  # Extract text from resume PDF
    job_text = extract_text_from_pdf(job_file)  # Extract text from job description PDF
    
    resume_json = parse_text(resume_text, "resume")  # Parse resume text into JSON
    job_json = parse_text(job_text, "job")  # Parse job text into JSON
    
    match_result = calculate_match(resume_json, job_json)  # Calculate match between resume and job
    suggestions = json.loads(generate_suggestions(resume_text, job_text, match_result))  # Generate and parse suggestions
    
    st.subheader("Results")         # Display results section header
    st.write(f"**Matching Score**: {match_result['matching_score']}%")  # Show matching score
    st.write("**Matching Skills**: ", match_result['matching_skills'])  # Show matching skills
    st.write("**Required Skills**: ", match_result['required_skills'])  # Show required skills
    st.write(f"**Experience Match**: {match_result['experience_match']} years")  # Show experience match
    st.write("**Suggestions**:")    # Display suggestions header
    for suggestion in suggestions:  # Loop through suggestions
        st.write(f"- {suggestion}")  # Display each suggestion as a bullet point