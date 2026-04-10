import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_similarity(resume_text, job_description):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)

    similarity_score = resume_doc.similarity(job_doc)
    return round(similarity_score*100,2)