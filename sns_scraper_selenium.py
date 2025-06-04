import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin, urlparse
import PyPDF2
import logging
from datetime import datetime
import re
import sys
from collections import defaultdict
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchDriverException

class TerminalProgressTracker:
    """Enhanced terminal progress tracking with real-time updates"""
    
    def __init__(self):
        self.stats = {
            'urls_scraped': 0,
            'pdfs_downloaded': 0,
            'buttons_clicked': 0,
            'errors': 0,
            'current_site': '',
            'current_url': '',
            'total_content_size': 0,  # Initialized to fix error
            'start_time': datetime.now()
        }
        self.lock = threading.Lock()
        self.last_update = time.time()
    
    def update_stats(self, **kwargs):
        with self.lock:
            self.stats.update(kwargs)
            self.print_progress()
    
    def increment(self, key, value=1):
        with self.lock:
            self.stats[key] += value
            self.print_progress()
    
    def print_progress(self):
        """Print real-time progress to terminal"""
        current_time = time.time()
        if current_time - self.last_update < 1.0:
            return
        self.last_update = current_time
        elapsed = datetime.now() - self.stats['start_time']
        print("\033[2K\r", end="")
        print(f"🔍 SCRAPING: {self.stats['current_site']} | "
              f"URLs: {self.stats['urls_scraped']} | "
              f"PDFs: {self.stats['pdfs_downloaded']} | "
              f"Buttons Clicked: {self.stats['buttons_clicked']} | "
              f"Errors: {self.stats['errors']} | "
              f"Time: {str(elapsed).split('.')[0]}", end="", flush=True)

class SNSFooterButtonScraper:
    def __init__(self):
        self.base_urls = [
            "https://www.snsgroups.com/",
            "https://www.snssquare.com/",
            "https://snsihub.ai/",
            "https://main.snsgroups.com/",
            "https://snsspine.in/",
            "https://snscourseware.org/"  # Assumed courseware site
        ]
        self.visited_urls = set()
        self.scraped_data = {
            "metadata": {
                "scraping_date": datetime.now().isoformat(),
                "total_urls_scraped": 0,
                "pdfs_downloaded": 0,
                "total_buttons_clicked": 0,
                "scraping_progress": []
            },
            "pages_data": [],
            "documents": [],
            "buttons": []
        }
        self.pdf_dir = "sns_pdfs"
        self.max_depth = 4
        self.delay = 1
        self.progress = TerminalProgressTracker()
        
        # Create directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)
        
        self.setup_logging()
        
        # Initialize Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except NoSuchDriverException as e:
            print(f"❌ ChromeDriver not found: {str(e)}")
            print("Please download ChromeDriver from https://chromedriver.chromium.org/downloads and place it in your PATH.")
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })

    def setup_logging(self):
        log_filename = f"logs/sns_scraping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        print(f"📋 Logging to: {log_filename}")

    def print_header(self):
        print("\n" + "="*80)
        print("🎯 SNS GROUPS FOOTER BUTTON SCRAPER")
        print("="*80)
        print("🌐 Target Websites:")
        for i, url in enumerate(self.base_urls, 1):
            print(f"   {i}. {url}")
        print(f"📁 PDF Directory: {self.pdf_dir}")
        print(f"🔍 Max Depth: {self.max_depth}")
        print(f"⏱️ Delay: {self.delay}s between requests")
        print("="*80)
        print("🚀 STARTING SCRAPING PROCESS...\n")

    def print_site_header(self, url, site_number, total_sites):
        print(f"\n{'='*60}")
        print(f"📍 SITE {site_number}/{total_sites}: {url}")
        print(f"{'='*60}")
        self.progress.update_stats(current_site=url)

    def is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            sns_domains = ['snsgroups.com', 'snssquare.com', 'snsihub.ai', 'snsspine.in', 'snscourseware.org']
            return any(domain in parsed.netloc for domain in sns_domains) and parsed.scheme in ['http', 'https']
        except:
            return False

    def categorize_url(self, url, page_content=""):
        url_lower = url.lower()
        if 'snscourseware.org' in url_lower:
            return 'courseware'
        elif any(keyword in url_lower for keyword in ['about', 'college', 'institution']):
            return 'institution'
        elif any(keyword in url_lower for keyword in ['admission', 'apply', 'course']):
            return 'admission'
        elif '.pdf' in url_lower:
            return 'document'
        else:
            return 'general'

    def download_pdf(self, pdf_url, source_url):
        try:
            print(f"\n📄 Downloading PDF: {pdf_url}")
            filename = os.path.basename(urlparse(pdf_url).path)
            if not filename or not filename.endswith('.pdf'):
                filename = f"document_{len(self.scraped_data['documents'])}.pdf"
            filepath = os.path.join(self.pdf_dir, filename)
            if os.path.exists(filepath):
                print(f"   ✓ Already exists: {filename}")
                return filepath, self.extract_pdf_text(filepath)
            response = self.session.get(pdf_url, timeout=30, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   📥 Downloading: {percent:.1f}%", end="", flush=True)
            print(f"\n   ✅ Downloaded: {filename} ({downloaded/1024:.1f} KB)")
            pdf_text = self.extract_pdf_text(filepath)
            self.progress.increment('pdfs_downloaded')
            self.logger.info(f"PDF downloaded: {filename}")
            return filepath, pdf_text
        except Exception as e:
            print(f"\n   ❌ Failed to download PDF: {str(e)}")
            self.logger.error(f"PDF download failed {pdf_url}: {e}")
            self.progress.increment('errors')
            return None, None

    def extract_pdf_text(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    try:
                        text += page.extract_text() + "\n"
                    except Exception as e:
                        print(f"   ⚠️ Error reading page {page_num}: {str(e)}")
                        continue
                return text.strip()
        except Exception as e:
            print(f"   ❌ Failed to extract PDF text: {str(e)}")
            return ""

    def scrape_page(self, url, depth=0, site_name="", is_footer_button_page=False):
        if url in self.visited_urls or depth > self.max_depth:
            return None
        self.visited_urls.add(url)
        self.progress.update_stats(current_url=url)
        print(f"\n🔍 [{depth}] Scraping: {url}")
        is_courseware = 'snscourseware.org' in url.lower()
        is_main_site = 'main.snsgroups.com' in url.lower()
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Allow dynamic content to load
            # Handle buttons (footer buttons for main site, all buttons otherwise)
            buttons = []
            button_data = []
            if is_main_site and depth == 0 and not is_footer_button_page:
                # Target footer buttons on main.snsgroups.com main page
                footer_selectors = [
                    'footer button',
                    'footer a.btn',
                    'footer a.button',
                    'footer a[class*="btn"]',
                    'footer a[class*="button"]',
                    '.footer button',
                    '.footer a.btn',
                    '.footer a.button',
                    '.footer a[class*="btn"]',
                    '.footer a[class*="button"]',
                    '.site-footer button',
                    '.site-footer a.btn',
                    '.site-footer a.button',
                    '.site-footer a[class*="btn"]',
                    '.site-footer a[class*="button"]'
                ]
                for selector in footer_selectors:
                    buttons.extend(self.driver.find_elements(By.CSS_SELECTOR, selector))
                print(f"   🖱️ Found {len(buttons)} footer buttons on {url}")
            else:
                # Click all buttons on other pages
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                buttons += self.driver.find_elements(By.CSS_SELECTOR, "a.btn, a.button, a[class*='btn'], a[class*='button']")
                print(f"   🖱️ Found {len(buttons)} buttons on {url}")
            for idx, button in enumerate(buttons):
                try:
                    button_text = button.text.strip()
                    if button_text:
                        button_href = button.get_attribute('href') or url
                        button_data.append({
                            "text": button_text,
                            "url": button_href,
                            "tag": button.tag_name,
                            "index": idx,
                            "is_footer_button": is_main_site and depth == 0 and not is_footer_button_page
                        })
                        print(f"   🖱️ Found button: '{button_text}' {'(footer)' if button_data[-1]['is_footer_button'] else ''}")
                        if button.is_displayed() and button.is_enabled():
                            try:
                                original_url = self.driver.current_url
                                button.click()
                                time.sleep(2)
                                new_url = self.driver.current_url
                                if new_url != original_url and self.is_valid_url(new_url) and new_url not in self.visited_urls:
                                    button_data[-1]["dynamic_url"] = new_url
                                    self.visited_urls.add(new_url)
                                    self.scrape_page(new_url, depth + 1, site_name, is_footer_button_page=True)
                                button_data[-1]["dynamic_content"] = self.driver.find_element(By.TAG_NAME, "body").text.strip()
                                self.progress.increment('buttons_clicked')
                                print(f"   🖱️ Clicked button: '{button_text}' {'(footer)' if button_data[-1]['is_footer_button'] else ''}")
                                self.driver.get(url)  # Return to original page
                            except WebDriverException as e:
                                print(f"   ⚠️ Could not click button '{button_text}': {str(e)}")
                except Exception as e:
                    print(f"   ⚠️ Error processing button {idx}: {str(e)}")
            self.scraped_data["buttons"].extend(button_data)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            page_data = {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "content": soup.get_text().strip(),
                "content_size": len(soup.get_text().strip()),
                "buttons": button_data,
                "links_found": 0,
                "category": self.categorize_url(url, soup.get_text()),
                "depth": depth,
                "site_name": site_name,
                "is_footer_button_page": is_footer_button_page
            }
            print(f"   📄 Title: {page_data['title'][:60]}...")
            print(f"   📊 Content size: {page_data['content_size']/1024:.1f} KB")
            print(f"   🏷️ Category: {page_data['category']}")
            print(f"   🖱️ Buttons found: {len(button_data)}")
            internal_links = []
            pdf_links = []
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                if href.lower().endswith('.pdf') or 'pdf' in href.lower():
                    pdf_links.append(href)
                elif self.is_valid_url(href) and href not in self.visited_urls:
                    internal_links.append(href)
            page_data["links_found"] = len(internal_links) + len(pdf_links)
            print(f"   🔗 Links found: {len(internal_links)} internal, {len(pdf_links)} PDFs")
            for pdf_url in pdf_links:
                pdf_path, pdf_content = self.download_pdf(pdf_url, url)
                if pdf_path and pdf_content:
                    self.scraped_data["documents"].append({
                        "type": "pdf",
                        "url": pdf_url,
                        "local_path": pdf_path,
                        "content": pdf_content,
                        "source_page": url,
                        "filename": os.path.basename(pdf_path),
                        "content_size": len(pdf_content)
                    })
            self.scraped_data["pages_data"].append(page_data)
            self.progress.increment('urls_scraped')
            self.progress.increment('total_content_size', page_data['content_size'])
            self.save_data_incremental(url)
            links_to_follow = internal_links if is_courseware else internal_links[:8]
            if links_to_follow:
                print(f"   🔄 Following {len(links_to_follow)} links...")
            for internal_url in links_to_follow:
                time.sleep(self.delay)
                self.scrape_page(internal_url, depth + 1, site_name, is_footer_button_page=False)
            return page_data
        except (TimeoutException, WebDriverException) as e:
            print(f"   ❌ Selenium error for {url}: {str(e)}")
            self.logger.error(f"Selenium error for {url}: {e}")
            self.progress.increment('errors')
            return None
        except Exception as e:
            print(f"   ❌ Scraping error: {str(e)}")
            self.logger.error(f"Scraping error for {url}: {e}")
            self.progress.increment('errors')
            return None

    def save_data_incremental(self, url):
        """Save scraped data incrementally after each page"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        complete_filename = f"snsfulldata_{timestamp}.json"
        try:
            with open(complete_filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            print(f"   💾 Incremental save completed: {complete_filename}")
        except Exception as e:
            print(f"   ❌ Failed to save incremental data: {str(e)}")
            self.logger.error(f"Incremental save failed for {url}: {e}")

    def scrape_all_sites(self):
        self.print_header()
        start_time = datetime.now()
        for i, base_url in enumerate(self.base_urls, 1):
            self.print_site_header(base_url, i, len(self.base_urls))
            try:
                site_name = urlparse(base_url).netloc
                self.scrape_page(base_url, site_name=site_name)
                print(f"\n✅ COMPLETED: {base_url}")
                print(f"   Pages scraped from this site: {len([p for p in self.scraped_data['pages_data'] if site_name in p['url']])}")
                time.sleep(3)
            except Exception as e:
                print(f"\n❌ FAILED: {base_url} - {str(e)}")
                self.logger.error(f"Site scraping failed {base_url}: {e}")
                continue
        self.print_final_summary(start_time)
        self.save_data()
        self.driver.quit()
        print(f"\n🎉 SCRAPING COMPLETED SUCCESSFULLY!")

    def print_final_summary(self, start_time):
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n{'='*80}")
        print("📊 FINAL SCRAPING SUMMARY")
        print(f"{'='*80}")
        print(f"⏱️ Total Duration: {str(duration).split('.')[0]}")
        print(f"🌐 Total URLs Scraped: {len(self.scraped_data['pages_data'])}")
        print(f"📄 Total PDFs Downloaded: {len(self.scraped_data['documents'])}")
        print(f"🖱️ Total Buttons Clicked: {len(self.scraped_data['buttons'])}")
        print(f"💾 Total Content Size: {sum(p.get('content_size', 0) for p in self.scraped_data['pages_data'])/1024/1024:.1f} MB")
        print(f"⚡ Average Rate: {len(self.scraped_data['pages_data'])/(duration.total_seconds()/60):.1f} pages/min")
        print(f"❌ Total Errors: {self.progress.stats['errors']}")
        site_stats = defaultdict(int)
        for page in self.scraped_data['pages_data']:
            site = urlparse(page['url']).netloc
            site_stats[site] += 1
        print(f"\n📍 BREAKDOWN BY SITE:")
        for site, count in site_stats.items():
            print(f"   {site}: {count} pages")
        footer_pages = [p for p in self.scraped_data['pages_data'] if p.get('is_footer_button_page')]
        if footer_pages:
            print(f"\n🏫 FOOTER BUTTON PAGES (main.snsgroups.com):")
            for i, page in enumerate(footer_pages[:5], 1):
                print(f"   {i}. {page['url']} ({page['title'][:50]}...)")
            if len(footer_pages) > 5:
                print(f"   ... and {len(footer_pages) - 5} more footer pages")
        if self.scraped_data['documents']:
            print(f"\n📄 PDFS DOWNLOADED:")
            total_pdf_size = 0
            for doc in self.scraped_data['documents'][:5]:
                size = doc.get('content_size', 0)
                total_pdf_size += size
                print(f"   📄 {doc['filename']} ({size/1024:.1f} KB)")
            if len(self.scraped_data['documents']) > 5:
                print(f"   ... and {len(self.scraped_data['documents']) - 5} more PDFs")
            print(f"   Total PDF content: {total_pdf_size/1024/1024:.1f} MB")
        print(f"{'='*80}")

    def save_data(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        print(f"\n💾 SAVING FINAL DATA...")
        complete_filename = f"snsfulldata_{timestamp}.json"
        print(f"   📁 Saving complete data: {complete_filename}")
        try:
            with open(complete_filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            print(f"   ✅ Data saved successfully!")
        except Exception as e:
            print(f"   ❌ Failed to save final data: {str(e)}")
            self.logger.error(f"Final save failed: {e}")

if __name__ == "__main__":
    scraper = SNSFooterButtonScraper()
    scraper.scrape_all_sites()