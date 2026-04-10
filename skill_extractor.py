from skills_db import SKILLS_DB

def extract_skills(cleaned_tokens):
    extracted_skills = []

    #Converting tokens to set for faster matching
    token_set = set(cleaned_tokens)

    for skill in SKILLS_DB:
        if " " in skill:
            skill_words = skill.split()
            if all(word in token_set for word in skill_words):
                extracted_skills.append(skill)
        else:
            if skill in token_set:
                extracted_skills.append(skill)
                
    return list(set(extracted_skills))
