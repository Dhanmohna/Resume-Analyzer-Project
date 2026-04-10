import streamlit as st
from groq import Groq

# 1. Initialize Groq instead of GenAI
# Securely replace this with your actual Groq API Key
client = Groq(api_key="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")

def analyze_resume_with_groq(resume_text, target_role):
    prompt = f"""
    Analyze the following resume for the target role: {target_role}

    1. Suggest top 3 suitable job roles (including how they align with {target_role}).
    2. List important missing skills for a {target_role} position.
    3. Give 3 specific improvement suggestions for the resume text.

    Resume:
    {resume_text}   
    """

    try:
        # Groq uses the 'chat.completions' format (similar to OpenAI)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional HR resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile", # Fastest and most reliable free model on Groq right now
        )
        return response.choices[0].message.content
    
    except Exception as e:
        if "429" in str(e):
            return "⚠️ Groq is temporarily busy (Rate Limit). Please wait 60 seconds and try again."
        return f"An error occurred: {e}"