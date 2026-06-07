import requests
import ast
import json
def extract_skills_using_ai(text):
    prompt=f"""
    You are an expert ATS parser and resume analyzer.

    Extract ALL professional skills explicitly mentioned in the text.

    Include:
    - Programming Languages
    - Frameworks
    - Libraries
    - Databases
    - Cloud Technologies
    - DevOps Tools
    - Software Tools
    - Business Skills
    - Analytical Skills
    - Consulting Skills
    - Soft Skills
    - Domain Skills

    Rules:
    1. Extract only skills explicitly mentioned.
    2. Do not infer skills.
    3. Preserve multi-word skills.
    4. Remove duplicates.
    5. Return ONLY a valid Python list.
    6. No explanations.
    7. No markdown.
    8. No headings. 
    Text: {text}"""
    response=requests.post("http://localhost:11434/api/generate",
    json={"prompt": prompt, "model": "llama3.2:3b", "stream": False})
    return ast.literal_eval(response.json()["response"])
def generate_suggestions(ats_score, matching_skills, missing_skills, bonus_skills, resume_text, jd_text):
    prompt=f"""
    You are a senior technical recruiter, ATS expert, and hiring manager.

    Candidate ATS Analysis

    ATS Score:
    {ats_score}

    Matched Skills:
    {matched_skills}

    Missing Skills:
    {missing_skills}

    Bonus Skills:
    {bonus_skills}

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    OBJECTIVE:

    Help the candidate maximize interview chances for this exact role.

    IMPORTANT RULES:

    1. top_missing_skills MUST contain ONLY skills from missing_skills.
    2. Never recommend skills already present in matched_skills.
    3. Never recommend skills already present in bonus_skills.
    4. Project suggestions must directly help acquire missing skills.
    5. Resume improvements must reference actual resume content.
    6. ATS tips must improve match with this JD.
    7. Avoid generic advice such as:
       - Take a course
       - Learn more
       - Improve skills
       - Gain experience
    8. Recommendations must be specific and actionable.
    9. Prioritize suggestions based on ATS impact.

    Return ONLY valid JSON.

    Output Format:

    {{
        "candidate_summary": "",

        "top_missing_skills": [],

        "project_suggestions": [],

        "resume_improvements": [],

        "ats_improvement_tips": []
    }}"""
    response=requests.post("http://localhost:11434/api/generate", json={"prompt": prompt, "model": "llama3.2:3b", "stream": False})
    print(response.json()["response"])
    return json.loads(response.json()["response"])