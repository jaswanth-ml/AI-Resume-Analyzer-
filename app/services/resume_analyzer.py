def analyze_resume(resume_skills,jd_skills):
    resume_skills=[skill.lower() for skill in resume_skills]
    jd_skills=[skill.lower() for skill in jd_skills]
    resume_skills=list(set(resume_skills))
    jd_skills=list(set(jd_skills))
    matched_skills=[]
    missing_skills=[]
    bonus_skills=[]
    for skill in jd_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    for skill in resume_skills:
        if skill not in jd_skills:
            bonus_skills.append(skill)
    matched_count = len(matched_skills)
    req_count=len(jd_skills)
    if req_count==0:
        ats_score=0
    else:
        ats_score=round((matched_count/req_count)*100,2)
    return {"ats_score": ats_score, "matched_skills": matched_skills, "missing_skills": missing_skills, "bonus_skills": bonus_skills}