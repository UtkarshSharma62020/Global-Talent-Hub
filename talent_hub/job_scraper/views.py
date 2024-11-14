# job_scraper/views.py
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Function to scrape job listings and filter those mentioning specified languages
def scrape_language_jobs(url):
    response = requests.get(url)  # Send a request to the provided URL
    
    if response.status_code != 200:
        return "Failed to retrieve the page", None

    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content

    jobs = []  # To store job listings

    # Get the entire text content of the page
    full_text = soup.get_text()

    # List of target languages
    target_languages = ['English', 'French', 'Hindi', 'Dutch']

    # Check if any target language is mentioned
    found_languages = [lang for lang in target_languages if lang in full_text]
    
    if found_languages:
        # Create a job dictionary with the updated description mentioning the found languages
        job = {
            'title': 'Job found',
            'description': f'<strong style="color: black;">Applicants proficient in {", ".join(found_languages)} are welcome; other languages not required.</strong>',
            'link': url
        }
        jobs.append(job)
    else:
        return "No jobs requiring the specified languages were found on this page.", None

    return None, jobs  # Return jobs that match the specified languages


def index(request):
    message = None
    jobs = None
    
    if request.method == 'POST':
        url = request.POST.get('url')
        message, jobs = scrape_language_jobs(url)

    return render(request, 'index.html', {'message': message, 'jobs': jobs})

from django.shortcuts import render
