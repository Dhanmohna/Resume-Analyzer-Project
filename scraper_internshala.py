import requests
from bs4 import BeautifulSoup

def scrape_internshala(role):
    query = role.replace(" ", "-").lower()
    url = f"https://internshala.com/jobs/{query}-jobs/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        jobs = []

        # ✅ Updated selector
        job_cards = soup.select("div.internship_meta")

        for job in job_cards[:10]:
            title = job.select_one("h3.heading_4_5")
            company = job.select_one("h4.heading_6")
            location = job.select_one("a.location_link")

            # link is outside sometimes → safe handling
            parent = job.find_parent("div", class_="individual_internship")
            link_tag = parent.find("a", href=True) if parent else None

            jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "description": f"{role} job from Internshala",
                "url": "https://internshala.com" + link_tag["href"] if link_tag else "#",
                "city": location.text.strip() if location else "N/A"
            })

        return jobs

    except Exception as e:
        print("Internshala Error:", e)
        return []