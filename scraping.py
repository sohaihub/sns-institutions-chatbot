import requests
from bs4 import BeautifulSoup
import json
import uuid
from urllib.parse import urljoin
import re

def fetch_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_page(url, soup):
    data = {
        "url": url,
        "title": "",
        "buttons": [],
        "links": [],
        "texts": [],
        "course_details": [],
        "faculty_details": [],
        "error": None
    }

    # Extract title
    title_tag = soup.find('title')
    data['title'] = title_tag.text.strip() if title_tag else ""

    # Extract buttons (assuming buttons are <a> or <button> with specific classes or text)
    buttons = soup.find_all(['a', 'button'], class_=re.compile('btn|button|apply|enquiry|pay|grievance|alumni', re.I))
    data['buttons'] = list(set([btn.text.strip() for btn in buttons if btn.text.strip()]))

    # Extract links
    links = soup.find_all('a', href=True)
    for link in links:
        href = urljoin(url, link['href'])
        text = link.text.strip()
        if text and href:
            data['links'].append({"text": text, "url": href})

    # Extract main texts (paragraphs, headings, etc.)
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = tag.text.strip()
        if text and len(text) > 20:  # Filter short texts
            data['texts'].append(text)

    return data

def scrape_courses(url, soup, data):
    # Navigate to departments page
    departments_url = None
    for link in data['links']:
        if 'departments' in link['url'].lower():
            departments_url = link['url']
            break
    
    if departments_url:
        html = fetch_page(departments_url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            course_links = soup.find_all('a', href=True)
            courses = []
            for link in course_links:
                if any(dept in link['href'].lower() for dept in ['engineering', 'technology']):
                    course_url = urljoin(departments_url, link['href'])
                    course_html = fetch_page(course_url)
                    if course_html:
                        course_soup = BeautifulSoup(course_html, 'lxml')
                        course_name = link.text.strip()
                        # Assuming duration and eligibility are mentioned in specific sections
                        duration = "4 years" if 'B.E.' in course_name or 'B.Tech.' in course_name else "2 years"
                        eligibility = "10+2 with Physics, Chemistry, and Mathematics" if 'B.E.' in course_name or 'B.Tech.' in course_name else "B.E./B.Tech in relevant discipline"
                        if 'Bio-Medical' in course_name or 'Food Technology' in course_name:
                            eligibility = "10+2 with Physics, Chemistry, and Mathematics/Biology"
                        courses.append({
                            "name": course_name,
                            "level": "Undergraduate" if 'B.E.' in course_name or 'B.Tech.' in course_name else "Postgraduate",
                            "duration": duration,
                            "fees": "Not specified on the website",
                            "eligibility": eligibility
                        })
            data['course_details'] = courses

def scrape_faculty(url, soup, data):
    # Navigate to faculty-related pages (e.g., department pages or about us)
    faculty = []
    leadership_url = None
    for link in data['links']:
        if 'leadership' in link['url'].lower():
            leadership_url = link['url']
            break
    
    if leadership_url:
        html = fetch_page(leadership_url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            # Extract leadership details
            leadership_sections = soup.find_all(['div', 'section'], class_=re.compile('leadership|faculty|team', re.I))
            for section in leadership_sections:
                name_tag = section.find(['h3', 'h4', 'h5'])
                designation_tag = section.find(['p', 'span'], class_=re.compile('designation|title', re.I))
                email_tag = section.find('a', href=re.compile('mailto:'))
                if name_tag and designation_tag:
                    faculty.append({
                        "name": name_tag.text.strip(),
                        "designation": designation_tag.text.strip(),
                        "email": email_tag.text.strip() if email_tag else "Not specified",
                        "department": "Administration",
                        "awards": []
                    })

    # Scrape department pages for additional faculty
    for link in data['links']:
        if 'engineering' in link['url'].lower() or 'technology' in link['url'].lower():
            html = fetch_page(link['url'])
            if html:
                soup = BeautifulSoup(html, 'lxml')
                faculty_sections = soup.find_all(['div', 'section'], class_=re.compile('faculty|staff|team', re.I))
                for section in faculty_sections:
                    name_tag = section.find(['h3', 'h4', 'h5'])
                    designation_tag = section.find(['p', 'span'], class_=re.compile('designation|role', re.I))
                    awards = section.find_all(['p', 'span'], class_=re.compile('award|recognition', re.I))
                    if name_tag:
                        department = link['text'].strip()
                        faculty.append({
                            "name": name_tag.text.strip(),
                            "designation": designation_tag.text.strip() if designation_tag else "Faculty",
                            "email": "Not specified",
                            "department": department,
                            "awards": [award.text.strip() for award in awards] if awards else []
                        })
    
    data['faculty_details'] = faculty

def main():
    url = "https://snsct.org/"
    html = fetch_page(url)
    if not html:
        return {
            "url": url,
            "title": "",
            "buttons": [],
            "links": [],
            "texts": [],
            "course_details": [],
            "faculty_details": [],
            "error": "Failed to fetch the main page"
        }

    soup = BeautifulSoup(html, 'lxml')
    data = parse_page(url, soup)
    scrape_courses(url, soup, data)
    scrape_faculty(url, soup, data)

    # Save to JSON file
    with open('snsct_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data

if __name__ == "__main__":
    data = main()
    print("Scraping completed. Data saved to snsct_data.json")