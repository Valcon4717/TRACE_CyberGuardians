import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from typing import List
import csv
import os 
import urllib.parse
#import aiofiles
import glob

class WebScraper:
    """
    Asynchronous web scraper to extract text content from web pages,
    including logos, labels, and class titles.

    Attributes:
        urls (list): List of URLs to scrape.
        concurrency (int): Maximum number of concurrent connections.

    Methods:
        scrape_pages(self, filename: str="scraped_output.csv") -> None

        async _fetch_url(self, url: str) -> str

        _extract_text_content(self, html: str) -> str

        async _scrape_pages_async(self) -> List
    """
    
    def __init__(self, concurrency: int=5, folder_path: str="database/ai/"):
        """
        Initialize with list of URLs and optional concurrency limit.
        
        Args:
            urls (list): List of URLs to scrape.
            concurrency (int): Max number of parallel fetches.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.folder_path = os.path.join(base_dir, folder_path)
        self.files = glob.glob(f"{self.folder_path}*.txt") + glob.glob(f"{self.folder_path}*.html")
        self.concurrency = concurrency
        self.filename = None
        

    async def scrape_pages(self, filename: str="scraped_output.csv")->None:
        """
        Public main method to run the async scraping from sync code.
        """
        data = await self._scrape_pages_async()
        filename = self.folder_path + filename
 
        # Save the results
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write a header for clarity
            csv_writer.writerow(['id', 'content', 'url'])
            csv_writer.writerows(data)
        print(f'[INFO] CSV file {filename} has been generated.')
        self.filename = filename
        return filename

    async def _fetch_file(self, file_path: str) -> str:
        """
        Fetch the HTML content of a single URL asynchronously.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The raw HTML text is successful, or an empty string if an error occurs.
        """
        # TODO: Update to fetch the URLs from the database.
        """
        try:
            async with aiofiles.open(url, 'r', encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            print(f"[ERROR] Could not fetch {url}")
            return ""
        """
        # TODO: Update path when fixed.
        """
        parsed_url = urllib.parse.urlparse(file_path)
        if parsed_url.scheme == "file":
            local_path = os.path.normpath(parsed_url.path)
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    return f.read()
                
            except Exception as e:
                print(f"[ERROR] Could not open local file: {e}")
                return ""
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(file_path) as response:
                        response.raise_for_status()
                        return await response.text()
            except aiohttp.ClientError as e:
                print(f"[ERROR] Could not fetch {file_path}: {e}")
                return 
                """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] Could not open local file: {e}")
            return ""     
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as e:
            print(f"[ERROR] Could not fetch {url}: {e}")
        """

    def _extract_text_content(self, html: str) -> str:
        """
        Parse the HTML and extract:
            - Text from <p>, <h1>, <h2>, <h3>, <span>
            - Logos: text from images (often used for logos).
            - Labels: text that is listed inside labels.
            - Class titles: any CSS class attributes from elements.

        Args:
            html (str): the HTML content to parse.
        
        Returns:
            str: A combined string of extracted text.
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Gather textual content from standard text tags
        text_parts = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'label', 'div', 'section', 'main', 'li', 'lu' ]):
            text_parts.append(tag.get_text(strip=True))
            
        # Gather "logo" text from <img alt="..">
        for img in soup.find_all("img"):
            alt_text = img.get("alt")
            if alt_text:
                text_parts.append(alt_text)

        # Gather aria-label or aria-labelledby attribues
        # aria-labelledby is an ID reference, so we do a basic attempt to extract it
        for element in soup.find_all(attrs={"aria-label": True}):
            text_parts.append(element.get("aria-label"))
        for element in soup.find_all(attrs={"aria-labelledby": True}):
            label_id = element.get('aria-labelledby')
            if label_id:
                ref = soup.find(id=label_id)
                if ref and ref.text:
                    text_parts.append(ref.text.strip())
        
        # Gather class attributes from all elements
        for el in soup.find_all(attrs={'class': True}):
            class_attr = el.get('class')
            # class_attr might be a list of classes; join them
            if class_attr and isinstance(class_attr, list):
                text_parts.append(" ".join(class_attr))

        # Merge everything into one string
        return " ".join(part for part in text_parts if part)
    

    async def _scrape_pages_async(self) -> List:
        """
        Asynchronoulsy scrape text content from all URLs in self.urls.

        Args:
            None

        Returns:
            list of tuples: [(id, content, url), ...]
        """
        results = []
        sem = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            async def scrape_page(i, file_path):

                print("file_path: ", file_path)
                async with sem:
                    content = await self._fetch_file(file_path)
                    if content:
                        if file_path.endswith('.html'):
                            text_content = self._extract_text_content(content)
                            results.append((i, text_content, file_path))
                        elif file_path.endswith('.txt'):
                            text_content = content
                            results.append((i, text_content, file_path))
                    else:
                        results.append((i, "", file_path))
                    
            tasks = []
            for i, url in enumerate(self.files, start=1):
                tasks.append(scrape_page(i, url))

            await asyncio.gather(*tasks)

        # Sort the final results by ID
        results.sort(key=lambda x: x[0])
        return results
    
    
        print(f"CSV file '{filename}' has been generated.")


async def test_scraper():
    scraper = WebScraper()
    test = await scraper.scrape_pages("scraped_output_test.csv")


if __name__ == "__main__":
    asyncio.run(test_scraper())
