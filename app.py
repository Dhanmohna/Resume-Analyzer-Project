import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from nlp_processor import clean_text
from skill_extractor import extract_skills
from matching_engine import calculate_similarity
#from jobs_data import JOBS
from groq_engine import analyze_resume_with_groq
import pandas as pd
import json
from scraper import scrape_jobs
from scraper_internshala import scrape_internshala
from scraper_remoteok import scrape_remoteok
from scoring_engine import calculate_skill_score, calculate_resume_score

REQUIRED_SKILLS = {
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "statistics"],
    "Software Engineer": ["java", "python", "c++", "data structures", "algorithms"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node"],
    "Data Analyst": ["excel", "sql", "power bi", "python"],
}

data = []

try:
    with open("jobs.ldjson", "r", encoding="utf-8") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except:
                continue   # skip bad lines

    jobs_df = pd.DataFrame(data)
    
    
except Exception as e:
    st.error(f"❌ Error loading dataset: {e}")

st.set_page_config(page_title="Intelligent Resume Analyzer",layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":    

    st.markdown(
        """
        <style>
        header {visibility: hidden;}
        body {
            background-image: url("https://static.vecteezy.com/system/resources/previews/000/633/705/original/abstract-gradient-geometric-background-simple-shapes-with-trendy-gradients-vector.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Optional: add a light transparent overlay to make text readable */
        .stApp {
            background-color: transparent;
        }

        .block-container {
                padding-top: 1.5rem;
            }

        div[data-testid="stFileUploader"] span {
            color: black !important;
            font-weight: 500;
        }

        div[data-testid="stFileUploader"] {
        
            background-color: white;
            padding: 10px 10px !important;
            border-radius: 8px;
            border-top:6px solid purple !important;
        }

        div[data-testid="stFileUploader"] label {
    display: none !important;
}

        div[data-baseweb="notification"] {
            background-color: #ffffff !important;
            color: #1b5e20 !important;
            border-left: 6px solid #2e7d32 !important;
            font-weight: 600;
        }

        div[data-testid="stFileUploader"] button {
            background-color: #7B2CBF !important;   /* Violet */
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
        }

        [data-testid="stFileUploaderDropzone"] {
    min-height: 20px !important; /* Default is ~200px, this cuts it by more than half */
    padding: 2px !important;
    display: flex;
    flex-direction: row !important; /* Makes items sit side-by-side to save space */
    align-items: center;
    justify-content: center;
    gap: 10px;
    
}

        div[data-baseweb="select"] > div {
            border-radius: 10px;
            font-size: 16px;
            border-top:rgb(239 29 76) solid 6px !important;
            
        }

        .custom-label {
        font-size: 20px;
        font-weight: bold;
        color: black;
        text-align:center;
        margin-bottom: 10px;
        margin-top: 20px;
    } 

      

/* Styling the button specifically inside the column */
div[data-testid="stButton"] > button {
    background-color: #5A189A !important; /* Professional Violet */
    color: white !important;
    font-size: 18px !important;
    font-weight: bold; /* Bold font weight */
    border-radius: 12px !important; /* Rounded corners */
    padding: 10px 10px !important;
    border: 2px solid #9D4EDD !important; /* Subtle border */
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
    text-transform: uppercase; /* Makes it look like a CTA */
    letter-spacing: 1px;
}

div[data-testid="stButton"] > button p{
color: white !important;
font-weight: bold;
}


/* Hover effect to make it interactive */
div[data-testid="stButton"] > button:hover {
    background-color: #5A189A !important; /* Darker purple on hover */
    border-color: #ffffff !important;
    transform: scale(1.03); /* Slight grow effect */
    box-shadow: 0px 6px 15px rgba(123, 44, 191, 0.4) !important;
}

/* Active/Click effect */
div[data-testid="stButton"] > button:active {
    transform: scale(0.98);
}

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align:center;'>Intelligent Resume Analyzer</h1>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center; color:purple; font-size:25px; font-weight:bold;'>"
        "Take your resume to the next level with AI-powered insights." 
    "</h3>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='color:white; font-size:17px;font-weight:bold;text-align:center;' >Our intelligent analyzer evaluates your skills, experience, and overall impact to generate a detailed score. Discover job matches tailored to your profile and receive actionable recommendations to strengthen your resume instantly.</p>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center; color:black; font-size:22px; font-weight:bold;margin-top:20px;'>"
        "Upload your resume to analyze job alignment "
        "</p>",
        unsafe_allow_html=True
    )


    uploaded_file = st.file_uploader(
        label="",
        type=["pdf","docx"]
    )

    st.markdown('<div class="custom-label">Select Target Job Role</div>', unsafe_allow_html=True)

    job_role = st.selectbox("",["Data Scientist","Software Engineer","Product Manager","UX Designer","DevOps Engineer","Cybersecurity Analyst","Cloud Architect","AI Researcher","Mobile App Developer","Full Stack Developer","Data Analyst","Machine Learning Engineer","Business Analyst","Project Manager","QA Engineer","Network Engineer","Database Administrator","Technical Writer","IT Support Specialist","Systems Administrator","Front-end Developer","Back-end Developer","Data Engineer","AI Engineer","Security Engineer","Cloud Engineer","UI/UX Designer","DevOps Specialist","Cybersecurity Specialist","Cloud Solutions Architect","AI Research Scientist","Mobile Developer","Full Stack Web Developer","Data Analyst","Machine Learning Scientist","Business Intelligence Analyst","Project Coordinator","QA Tester","Network Administrator","Database Manager","Technical Communicator","IT Support Technician","Systems Engineer"],label_visibility="collapsed")

    # Create 3 columns with a 1:1:1 ratio
    col1, col2, col3 = st.columns([1, 1, 1])

    if uploaded_file:
        st.toast("Resume File Uploaded Successfully!", icon="✅")
        file_type = uploaded_file.name.split(".")[-1]
        
        if(file_type) == "pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text

        elif(file_type) == "docx":
            resume_text = extract_text_from_docx(uploaded_file)
            st.session_state.resume_text = resume_text

        else:
            st.toast("Unsupported file type. Please upload a PDF or DOCX file.",icon="🚫")
            resume_text = ""
    
    
    with col2: # This places the button in the center column
        if st.button("Analyze Resume", use_container_width=True):
            if uploaded_file:
                st.session_state.page = "analysis"
                st.session_state.file = uploaded_file
                st.session_state.role = job_role
                st.rerun() 
            else:
                st.toast("Please upload a resume file first!", icon="🚫")
    

elif st.session_state.page == "analysis": 
    st.set_page_config(page_title="Intelligent Resume Analyzer",layout="wide")
 
    st.markdown("""
        <style>
        .stApp { background-image: none !important; background-color: white !important; }
        header { visibility: visible !important; }
                body{
                 text-align: center !important;
                }
        h1, h2, h3, h4, p, span { color: #1E1E1E !important; }
                [data-testid="stHeader"] h1 {
    color: purple;
    text-align: center;
    font-family: 'Arial';
    font-size: 42px;
}

                div[data-testid="stAppViewBlockContainer"] {
            max-width: 95% !important;
            width: 95% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* This targets the vertical block specifically to stop it from 'pinching' the top */
        [data-testid="stVerticalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Since the page is now wide, we manually center the header text so it doesn't hug the left wall */
        .analysis-title {
            text-align: center;
            width: 100%;
            padding-bottom: 20px;
        }
        
        /* Make the metrics look professional and spaced out */
        [data-testid="stMetric"] {
            text-align: center;
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 10px;
        }

                /* Create a container that pushes items to opposite walls */
.extreme-flex-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
    padding: 0;
}

.left-stat {
    text-align: left;
}

.right-stat {
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end; /* This forces the content to the right wall */
}

/* Ensure the subheaders don't have extra margins pushing them away */
.extreme-flex-container h3 {
    margin-top: 0 !important;
}
        </style>
    """, unsafe_allow_html=True)
    uploaded_file = st.session_state.get("file")
    job_role = st.session_state.get("role") 
    resume_text = st.session_state.get("resume_text")   

    # Navigation Header
    with st.container():
        col_back, col_title, col_empty = st.columns([1, 6, 1])
        with col_back:
            if st.button("⬅️ Back"):
                st.session_state.page = "home"
                st.rerun()
        with col_title:
            st.markdown(f"<h1 style='text-align: center; color: purple;'>Analysis for {job_role}</h1>", unsafe_allow_html=True)

    if uploaded_file is not None:
        if resume_text:        
               # st.subheader("Extracted Resume Text:")
               # st.text_area("Resume Content", resume_text, height=300)

                cleaned_tokens = clean_text(resume_text)
                # st.subheader("Processed Tokens:")
                # st.write(cleaned_tokens)

                skills = extract_skills(cleaned_tokens)
                # st.subheader("Extracted Skills:")
                # st.write(skills)



                #Calculate Score
                required = REQUIRED_SKILLS.get(job_role, [])
                skill_score = calculate_skill_score(skills, required)

                #Skill Gap Analysis

                missing_skills = list(set(required) - set(skills))

                # --- 4. SCORE & SKILL GAP (Top Section) ---
                col_score, col_gap = st.columns([1, 1])

                with col_score:
                    st.subheader("📊 Performance Score")
                    # We calculate final_score later based on similarity, 
                    # but we can show skill match immediately
                    st.metric(label="Skill Match", value=f"{skill_score:.1f}%")
                    
                with col_gap:
                    st.subheader("⚠️ Skill Gap")
                    if missing_skills:
                        # Using a bulleted list for clean look (no tables as per your style!)
                        for s in missing_skills:
                            st.write(f"❌ Missing: **{s.capitalize()}**")
                    else:
                        st.success("🎯 Perfect match for core skills!")

                st.divider()

                # st.subheader("⚠️ Skill Gap Analysis")

                # if missing_skills:
                #     st.write("You are missing these important skills:")
                #     st.write(missing_skills)
                # else:
                #     st.success("Great! You match all required skills 🎯")

                # Job Matching
    st.subheader("Job Matching Results:")

    results = []

    # -------------------------------
    # 1️⃣ DATASET (Indeed Kaggle)
    # -------------------------------
    filtered_jobs = jobs_df[
        jobs_df["job_title"].str.contains(job_role, case=False, na=False)
    ].head(50)

    for _, job in filtered_jobs.iterrows():
        if pd.isna(job["job_description"]):
            continue

        similarity_score = calculate_similarity(resume_text, job["job_description"])

        results.append({
            "title": job["job_title"],
            "company": job["company_name"],
            "description": job["job_description"],
            "url": job["url"],
            "similarity_score": similarity_score,
            "source": "Indeed Dataset"
        })

    # -------------------------------
    # 2️⃣ INTERNSHALA SCRAPING
    # -------------------------------
    try:
        internshala_jobs = scrape_internshala(job_role)

        for job in internshala_jobs:
            similarity_score = calculate_similarity(resume_text, job["description"])

            results.append({
                "title": job["title"],
                "company": job["company"],
                "description": job["description"],
                "url": job["url"],
                "similarity_score": similarity_score,
                "source": "Internshala"
            })
    except:
        st.warning("Internshala scraping failed")

    # -------------------------------
    # 3️⃣ REMOTEOK SCRAPING
    # -------------------------------
    try:
        remote_jobs = scrape_remoteok(job_role)

        for job in remote_jobs:
            similarity_score = calculate_similarity(resume_text, job["description"])

            results.append({
                "title": job["title"],
                "company": job["company"],
                "description": job["description"],
                "url": job["url"],
                "similarity_score": similarity_score,
                "source": "RemoteOK"
            })
    except:
        st.warning("RemoteOK scraping failed")

    # -------------------------------
    # 🔥 FINAL SORTING
    # -------------------------------
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    similarity_score = results[0]["similarity_score"] if results else 0
    final_score = calculate_resume_score(similarity_score, skill_score)
    st.subheader("📊 Resume Score")

    st.markdown(f"""
    <div style="
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        text-align:center;
    ">
    <h2>Resume Score: {final_score:.2f} / 100</h2>
    <p>Skill Match: {skill_score:.2f}%</p>
    <p>Job Similarity: {similarity_score:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

    
    # -------------------------------
    # 🎯 DISPLAY TOP JOBS
    # -------------------------------
    for job in results[:15]:
        st.markdown(f"""
        <div style="
            background-color: white; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">

        <h4>{job['title']}</h4>
        <p style='color:purple; font-weight:bold;'>{job['company']}</p>

        <p><strong>Source:</strong> {job['source']}</p>

        <p><strong>Similarity Score:</strong> {job['similarity_score']}%</p>

        <p>{job['description'][:200]}...</p>

        <a href="{job['url']}" target="_blank">🔗 View Job</a>

        </div>
        """, unsafe_allow_html=True)
                    
        # #Gemini Analysis
        # st.subheader("AI Smart Career Analysis:")

        # if st.button("AI Career Analysis"):
        #     if resume_text and job_role:
                
        #         with st.spinner("Analyzing resume with AI..."):
        #             ai_response = analyze_resume_with_groq(resume_text, job_role)
        #             st.markdown(f"""
        #         <div style="
        #     background-color: #f0f8ff; 
        #     padding: 15px; 
        #     border-radius: 10px; 
        #     margin-bottom: 15px;
        #     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        #         ">
        #         <h5 style='margin:0;font-weight:bold;'>AI Career Analysis</h5>
        #         <p style='margin:5px 0;'>{ai_response}</p>
        #     </div>
        #     """, unsafe_allow_html=True)

        # else:
        #     st.error("Could not extract text from resume")
    