#!/usr/bin/env python3

import argparse
import sys
import re
from typing import Dict, List, Set
from tqdm import tqdm
from urllib.parse import urlparse, urljoin

from crawler import Crawler
from markdown_converter import MarkdownConverter
from file_handler import FileHandler


class DocRepo:
    def __init__(self, base_url: str, output_dir: str = "docrepo", max_depth: int = 3, 
                 delay: float = 0.5, download_images: bool = True, respect_robots_txt: bool = True):
        """
        Initialize the documentation repository generator.
        
        Args:
            base_url: The starting URL to crawl
            output_dir: Directory to save documentation
            max_depth: Maximum depth of links to follow
            delay: Delay between requests in seconds
            download_images: Whether to download images
            respect_robots_txt: Whether to respect robots.txt rules
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.delay = delay
        self.should_download_images = download_images
        self.respect_robots_txt = respect_robots_txt
        
        print(f"Initializing DocRepo with base URL: {base_url}")
        print(f"Output directory: {output_dir}")
        print(f"Max crawl depth: {max_depth}")
        print(f"Download images: {download_images}")
        print(f"Respect robots.txt: {respect_robots_txt}")
        
        # Initialize components
        self.crawler = Crawler(base_url, max_depth, delay, self.respect_robots_txt)
        self.file_handler = FileHandler(output_dir)
        self.converter = None  # Will be initialized after crawling
        
        # URL to local file map (for link rewriting)
        self.url_to_file_map: Dict[str, str] = {}
        
        # Image URL to local file map
        self.image_map: Dict[str, str] = {}
    
    def extract_images_from_markdown(self, markdown: str, base_url: str) -> List[str]:
        """
        Extract image URLs from markdown content.
        
        Args:
            markdown: Markdown content
            base_url: Base URL for resolving relative image paths
            
        Returns:
            List of image URLs
        """
        # Regular expression for markdown image syntax
        image_pattern = r'!\[.*?\]\(([^)]+)\)'
        image_urls = []
        
        for match in re.finditer(image_pattern, markdown):
            image_url = match.group(1)
            # Resolve relative URLs
            absolute_url = urljoin(base_url, image_url)
            image_urls.append(absolute_url)
        
        return image_urls
    
    def download_images(self, markdown: str, base_url: str) -> str:
        """
        Download images from markdown content and replace URLs.
        
        Args:
            markdown: Markdown content
            base_url: Base URL for resolving relative image paths
            
        Returns:
            Markdown with updated image URLs
        """
        if not self.should_download_images:
            return markdown
        
        image_urls = self.extract_images_from_markdown(markdown, base_url)
        
        # Regular expression for markdown image syntax
        image_pattern = r'(!\[.*?\]\()([^)]+)(\))'
        
        def replace_image_url(match):
            alt_text_part = match.group(1)
            image_url = match.group(2)
            closing_part = match.group(3)
            
            # Resolve relative URLs
            absolute_url = urljoin(base_url, image_url)
            
            # Check if image already downloaded
            if absolute_url in self.image_map:
                local_path = self.image_map[absolute_url]
            else:
                # Download the image
                try:
                    local_path = self.file_handler.download_image(absolute_url)
                    self.image_map[absolute_url] = local_path
                except Exception as e:
                    print(f"Error downloading image {absolute_url}: {e}")
                    local_path = image_url  # Keep original URL if download fails
            
            return f"{alt_text_part}{local_path}{closing_part}"
        
        # Replace image URLs in markdown
        return re.sub(image_pattern, replace_image_url, markdown)
    
    def run(self) -> None:
        """Run the full documentation generation process."""
        # Step 1: Crawl the website
        print("Step 1: Crawling website...")
        crawl_results = self.crawler.crawl()
        
        if not crawl_results:
            print("Error: No content was crawled. Check the URL and try again.")
            return
        
        print(f"Crawled {len(crawl_results)} pages.")
        
        # Step 2: Generate filenames and build URL to file mapping
        print("Step 2: Generating filenames...")
        for url in tqdm(crawl_results.keys()):
            filename = self.file_handler.generate_unique_filename(url)
            self.url_to_file_map[url] = filename
        
        # Step 3: Initialize converter with URL mapping
        self.converter = MarkdownConverter(self.url_to_file_map)
        
        # Step 4: Convert HTML to Markdown and save files
        print("Step 3: Converting to Markdown and saving files...")
        for url, data in tqdm(crawl_results.items()):
            html_content = data['content']
            title = data['title']
            
            # Convert to markdown
            markdown = self.converter.convert_html_to_markdown(html_content, url)
            
            # Download images and update markdown
            if self.should_download_images:
                markdown = self.download_images(markdown, url)
            
            # Add front matter
            markdown_with_frontmatter = self.converter.add_front_matter(markdown, title, url)
            
            # Save to file
            self.file_handler.save_markdown(url, markdown_with_frontmatter)
        
        # Step 5: Create index file
        print("Step 4: Creating index file...")
        url_title_map = {url: data['title'] for url, data in crawl_results.items()}
        index_file = self.file_handler.create_index(url_title_map)
        
        print(f"Documentation repository created successfully in {self.output_dir}")
        print(f"Open {self.output_dir}/{index_file} to view the documentation")


def main():
    parser = argparse.ArgumentParser(description='Generate a documentation repository from a website.')
    parser.add_argument('url', help='The base URL to crawl')
    parser.add_argument('-o', '--output', default='docrepo', help='Output directory (default: docrepo)')
    parser.add_argument('-d', '--depth', type=int, default=3, help='Maximum depth to crawl (default: 3)')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests in seconds (default: 0.5)')
    parser.add_argument('--no-images', action='store_true', help='Do not download images')
    parser.add_argument('--ignore-robots', action='store_true', help='Ignore robots.txt restrictions')
    
    args = parser.parse_args()
    
    # Validate URL
    try:
        result = urlparse(args.url)
        if not all([result.scheme, result.netloc]):
            print("Error: Invalid URL. Please provide a complete URL with scheme (e.g., http:// or https://).")
            sys.exit(1)
    except ValueError:
        print("Error: Invalid URL format.")
        sys.exit(1)
    
    try:
        doc_repo = DocRepo(
            base_url=args.url,
            output_dir=args.output,
            max_depth=args.depth,
            delay=args.delay,
            download_images=not args.no_images,
            respect_robots_txt=not args.ignore_robots
        )
        doc_repo.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 