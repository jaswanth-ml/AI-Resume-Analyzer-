from services.ai_service import extract_skills_using_ai
text=""" python fastapi docker aws n8n openai"""
skills=extract_skills_using_ai(text)
print(skills)
print(type(skills))