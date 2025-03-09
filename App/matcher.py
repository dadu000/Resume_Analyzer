import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_json, job_json):
    resume_data = json.loads(resume_json)
    job_data = json.loads(job_json)
    
    resume_skills = " ".join(resume_data["skills"])
    job_skills = " ".join(job_data["skills"])
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_skills, job_skills])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    matching_score = similarity * 100
    matching_skills = [skill for skill in resume_data["skills"] if skill in job_data["skills"]]
    experience_match = min(resume_data["experience"], job_data["experience"])
    
    return {
        "matching_score": round(matching_score, 2),
        "matching_skills": matching_skills,
        "required_skills": job_data["skills"],
        "experience_match": experience_match
    }