import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import logging
from urllib.robotparser import RobotFileParser
import os

class IndeedScraper:
    def __init__(self, base_url="https://ae.indeed.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.setup_logging()
        self.check_robots_txt()

    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            filename='scraper.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def check_robots_txt(self):
        """Check robots.txt for permissions"""
        rp = RobotFileParser()
        rp.set_url(f"{self.base_url}/robots.txt")
        try:
            rp.read()
            if not rp.can_fetch(self.headers['User-Agent'], self.base_url):
                logging.warning("Scraping not allowed according to robots.txt")
                return False
            return True
        except Exception as e:
            logging.error(f"Error checking robots.txt: {str(e)}")
            return False

    def scrape_job_titles(self):
        """Scrape job titles from Indeed"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            job_titles = soup.find_all('h2', class_='jobTitle')
            
            titles = []
            for job in job_titles:
                titles.append(job.get_text().strip())
            
            return titles

        except requests.RequestException as e:
            logging.error(f"Error fetching data: {str(e)}")
            return []

    def save_to_csv(self, data):
        """Save scraped data to CSV file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'indeed_jobs_{timestamp}.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Job Title', 'Timestamp'])
                
                for title in data:
                    writer.writerow([title, datetime.now().isoformat()])
                    
            logging.info(f"Data successfully saved to {filename}")
            return filename
        
        except IOError as e:
            logging.error(f"Error saving to CSV: {str(e)}")
            raise

def main():
    """Main function to run the scraper"""
    scraper = IndeedScraper()
    
    try:
        logging.info("Starting scraping process")
        titles = scraper.scrape_job_titles()
        
        if titles:
            output_file = scraper.save_to_csv(titles)
            print(f"Scraping completed successfully. Data saved to {output_file}")
        else:
            print("No job titles found")
            
    except Exception as e:
        logging.error(f"Scraping failed: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
