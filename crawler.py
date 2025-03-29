import requests
import time
import urllib.robotparser
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Set, List, Dict, Optional


class Crawler:
    def __init__(self, 
                 base_url: str, 
                 max_depth: int = 3, 
                 delay: float = 0.5, 
                 respect_robots_txt: bool = True):
        """
        Initialize the crawler with the base URL and configuration.
        
        Args:
            base_url: The starting URL to crawl
            max_depth: Maximum depth of links to follow
            delay: Delay between requests in seconds
            respect_robots_txt: Whether to respect robots.txt rules
        """
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.respect_robots_txt = respect_robots_txt
        self.visited_urls: Set[str] = set()
        self.url_contents: Dict[str, str] = {}
        self.url_titles: Dict[str, str] = {}
        
        # Parse the base domain for robots.txt
        parsed_url = urlparse(base_url)
        self.base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Initialize robots parser if needed
        self.robot_parser = None
        if self.respect_robots_txt:
            self.robot_parser = urllib.robotparser.RobotFileParser()
            self.robot_parser.set_url(urljoin(self.base_domain, '/robots.txt'))
            try:
                self.robot_parser.read()
            except Exception as e:
                print(f"Warning: Could not read robots.txt: {e}")
    
    def is_allowed(self, url: str) -> bool:
        """Check if the URL is allowed to be crawled according to robots.txt."""
        if not self.respect_robots_txt or self.robot_parser is None:
            return True
        return self.robot_parser.can_fetch("*", url)
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and resolving relative URLs."""
        parsed = urlparse(url)
        # Remove fragments
        clean_url = parsed._replace(fragment="").geturl()
        return clean_url

    def extract_links(self, url: str, html_content: str) -> List[str]:
        """Extract links from HTML content that are on the same domain."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Find all anchor tags
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(url, href)
            normalized_url = self.normalize_url(absolute_url)
            
            # Only include links from the same domain
            if urlparse(normalized_url).netloc == urlparse(self.base_url).netloc:
                links.append(normalized_url)
        
        return links
    
    def extract_title(self, html_content: str) -> str:
        """Extract the title from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text() if title_tag else "Untitled Page"
    
    def crawl(self) -> Dict[str, Dict]:
        """
        Crawl the website starting from the base URL up to the specified depth.
        
        Returns:
            Dictionary mapping URLs to their content, title, and other metadata
        """
        to_crawl = [(self.base_url, 0)]  # (url, depth)
        
        if not self.respect_robots_txt:
            print("Warning: robots.txt is being ignored.")
        
        while to_crawl:
            url, depth = to_crawl.pop(0)
            
            # Skip if already visited or exceeds max depth
            if url in self.visited_urls or depth > self.max_depth:
                continue
            
            # Skip if not allowed by robots.txt
            if not self.is_allowed(url):
                print(f"Skipping {url} (disallowed by robots.txt)")
                continue
            
            print(f"Crawling {url} (depth {depth})")
            self.visited_urls.add(url)
            
            try:
                response = requests.get(url, headers={'User-Agent': 'DocRepo Crawler'})
                response.raise_for_status()
                
                # Store content and title
                html_content = response.text
                self.url_contents[url] = html_content
                self.url_titles[url] = self.extract_title(html_content)
                
                # If we haven't reached max depth, extract links and add to crawl queue
                if depth < self.max_depth:
                    links = self.extract_links(url, html_content)
                    for link in links:
                        if link not in self.visited_urls:
                            to_crawl.append((link, depth + 1))
                
                # Respect the delay between requests
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        
        # Compile results
        results = {}
        for url in self.visited_urls:
            if url in self.url_contents:
                results[url] = {
                    'content': self.url_contents[url],
                    'title': self.url_titles.get(url, "Untitled Page")
                }
        
        return results 