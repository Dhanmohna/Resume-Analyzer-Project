import requests
from bs4 import BeautifulSoup

def scrape_remoteok(role):
    url = "https://remoteok.com/remote-dev-jobs"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        jobs = []

        job_rows = soup.find_all("tr", class_="job")

        for job in job_rows[:10]:
            title = job.find("h2")
            company = job.find("h3")
            link = job.get("data-href")

            jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "description": f"{role} job (RemoteOK)",
                "url": "https://remoteok.com" + link if link else "#",
                "city": "Remote",
                "job_type": "Remote"
            })

        return jobs

    except Exception as e:
        print("RemoteOK Error:", e)
        return []