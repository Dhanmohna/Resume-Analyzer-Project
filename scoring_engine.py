def calculate_skill_score(extracted_skills, required_skills):
    match = 0
    for skill in required_skills:
        if skill.lower() in [s.lower() for s in extracted_skills]:
            match += 1
    return (match / len(required_skills)) * 100 if required_skills else 0


def calculate_resume_score(similarity_score, skill_score):
    return (0.6 * similarity_score) + (0.4 * skill_score)

