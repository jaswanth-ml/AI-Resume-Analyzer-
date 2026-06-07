from fastapi import FastAPI, UploadFile, File, Form
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import extract_skills_using_ai
from app.services.ai_service import generate_suggestions
from app.services.resume_analyzer import analyze_resume
app=FastAPI()
@app.post("/analyze")
def analyze(resume: UploadFile=File(...),jd_text: str=Form(...)):
    resume_text=extract_text_from_pdf(resume.file)
    resume_skills=extract_skills_using_ai(resume_text)
    jd_skills=extract_skills_using_ai(jd_text)
    result=analyze_resume(resume_skills,jd_skills)
    suggestions=generate_suggestions(result["ats_score"],result["matched_skills"],result["missing_skills"],result["bonus_skills"],resume_skills,jd_skills)
    result["suggestions"]=suggestions
    return result