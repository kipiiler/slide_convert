import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re

class SlideScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.download_dir = "slides"
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_schedule_page(self):
        """Fetch the schedule page content"""
        response = self.session.get(self.base_url)
        response.raise_for_status()
        return response.text

    def extract_slide_links(self, html_content):
        """Extract all PDF slide links from the schedule page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        slide_links = []
        
        # Find all links in the table
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.pdf'):
                # Handle relative URLs
                full_url = urljoin(self.base_url, href)
                slide_name = link.text.strip() if link.text else os.path.basename(href)
                slide_links.append({
                    'url': full_url,
                    'name': slide_name
                })
        
        return slide_links

    def download_slide(self, slide_info):
        """Download a single slide PDF"""
        try:
            response = self.session.get(slide_info['url'])
            response.raise_for_status()
            
            # Create a safe filename
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', slide_info['name'])
            if not safe_filename.endswith('.pdf'):
                safe_filename += '.pdf'
                
            filepath = os.path.join(self.download_dir, safe_filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {safe_filename}")
            return True
        except Exception as e:
            print(f"Error downloading {slide_info['name']}: {str(e)}")
            return False

    def download_all_slides(self):
        """Download all slides from the schedule"""
        print("Fetching schedule page...")
        html_content = self.get_schedule_page()
        
        print("Extracting slide links...")
        slide_links = self.extract_slide_links(html_content)
        
        print(f"Found {len(slide_links)} slides to download")
        successful_downloads = 0
        
        for slide_info in slide_links:
            if self.download_slide(slide_info):
                successful_downloads += 1
        
        print(f"\nDownload complete!")
        print(f"Successfully downloaded {successful_downloads} out of {len(slide_links)} slides")
        print(f"Slides are saved in the '{self.download_dir}' directory")

    def get_links(self, keyword):
        html_content = self.get_schedule_page()
        links = self.extract_slide_links(html_content)
        if keyword is None:
            return links

        # filter links by keyword for name
        return [link for link in links if keyword in link['name']]
            

if __name__ == "__main__":
    # Example usage
    course_url = "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"
    scraper = SlideScraper(course_url)
    links = scraper.get_links("slides")
    print(links)

