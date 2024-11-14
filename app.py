from flask import Flask, request, render_template, jsonify
import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/search_jobs')
def search_jobs():
    skills = request.args.get('skills')
    encoded_skills = requests.utils.quote(skills)
    
    job_listings = []
    
    # Call the scraper functions
    job_listings.extend(scrape_internshala(encoded_skills))  
    job_listings.extend(scrape_we_work_remotely_selenium(encoded_skills))
    job_listings.extend(scrape_jobspresso(encoded_skills))  
    
    limited_job_listings = job_listings[:10]
    print("Job listings:", limited_job_listings)
    
    return jsonify(limited_job_listings)

def scrape_internshala(skills):
    url = f"https://www.internshala.com/internships/keywords-{skills}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve the Internshala page")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('div', class_='individual_internship')
    job_listings = []

    for job_card in job_cards[:10]:  # Limit to 10 jobs
        title_element = job_card.find('a', class_='job-title-href')
        title = title_element.text.strip() if title_element else "Title not available"
        job_link = "https://www.internshala.com" + title_element['href'] if title_element else "#"

        company_element = job_card.find('a', class_="company_and_premium")
        company = company_element.text.strip() if company_element else "Company not available"

        location_element = job_card.find('div', class_='row-1-item locations')
        location = location_element.text.strip() if location_element else "Location not available"

        platform_choice = random.choice(['LinkedIn', 'Internshala'])
        
        job_listings.append({
            'title': title,
            'company': company,
            'location': location,
            'link': job_link,
            'platform': platform_choice
        })
    
    return job_listings



def scrape_we_work_remotely_selenium(skills):
    url = f"https://weworkremotely.com/remote-jobs/search?term={skills}"
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        # Wait for the job listings to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs"))
        )

        # Wait for a bit longer to ensure the page is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "feature"))
        )
        
        # Once the page is loaded, grab the HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    except Exception as e:
        print(f"Error fetching We Work Remotely data: {e}")
        driver.quit()
        return []

    driver.quit()

    # Parse the job listings
    job_listings = []
    job_sections = soup.find_all('section', class_='jobs')

    # Ensure we get all the job listings correctly
    for section in job_sections:
        job_cards = section.find_all('li', class_='feature')
        
        for job_card in job_cards[:10]:
            title = job_card.find('span', class_='title').text.strip() if job_card.find('span', 'title') else "Title not available"
            job_link = "https://weworkremotely.com" + job_card.find('a')['href'] if job_card.find('a') else "#"
            company = job_card.find('span', class_='company').text.strip() if job_card.find('span', 'company') else "Company not available"
            location = job_card.find('div', class_='region company').text.strip() if job_card.find('div', 'region company') else "Location not available"

            job_listings.append({
                'title': title,
                'company': company,
                'location': location,
                'link': job_link,
                'platform': 'We Work Remotely'
            })

    return job_listings

def scrape_jobspresso(skills):
    url = f"https://jobspresso.co/?s={skills}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve Jobspresso data")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('article', class_='job_listing')

    job_listings = []
    for job_card in job_cards[:10]:
        title_element = job_card.find('h3')
        title = title_element.text.strip() if title_element else "Title not available"
        job_link = job_card.find('a')['href'] if job_card.find('a') else "#"

        company_element = job_card.find('span', class_='company')
        company = company_element.text.strip() if company_element else "Company not available"

        location_element = job_card.find('div', class_='location')
        location = location_element.text.strip() if location_element else "Location not available"
        
        job_listings.append({
            'title': title,
            'company': company,
            'location': location,
            'link': job_link,
            'platform': 'Jobspresso'
        })
    
    return job_listings

def scrape_remote_ok(skills):
    url = f"https://remoteok.com/remote-{skills}-jobs"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve Remote OK data")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('tr', class_='job')
    
    job_listings = []
    for job_card in job_cards[:10]:
        title_element = job_card.find('h2', itemprop='title')
        title = title_element.text.strip() if title_element else "Title not available"
        job_link = "https://remoteok.com" + job_card.find('a', itemprop='url')['href'] if job_card.find('a', itemprop='url') else "#"

        company_element = job_card.find('h3', itemprop='name')
        company = company_element.text.strip() if company_element else "Company not available"

        location = "Remote"  # Most jobs on Remote OK are remote
        
        job_listings.append({
            'title': title,
            'company': company,
            'location': location,
            'link': job_link,
            'platform': 'Remote OK'
        })
    
    return job_listings

if __name__ == "__main__":
    app.run(debug=True)
