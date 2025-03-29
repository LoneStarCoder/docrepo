import html2text
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Tuple


class MarkdownConverter:
    def __init__(self, link_map: Dict[str, str] = None):
        """
        Initialize the Markdown converter.
        
        Args:
            link_map: A dictionary mapping original URLs to local file paths
        """
        self.link_map = link_map or {}
        self.h2t = html2text.HTML2Text()
        self.configure_converter()
    
    def configure_converter(self):
        """Configure the HTML2Text converter with appropriate settings."""
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_tables = False
        self.h2t.body_width = 0  # No wrapping
        self.h2t.protect_links = True
        self.h2t.unicode_snob = True
        self.h2t.inline_links = True
        self.h2t.wrap_links = False
    
    def extract_images(self, html_content: str, base_url: str) -> Tuple[str, List[Dict]]:
        """
        Extract image references from HTML content.
        
        Args:
            html_content: Raw HTML content
            base_url: Base URL for resolving relative paths
            
        Returns:
            Tuple containing:
            - Modified HTML with processed image tags
            - List of dictionaries with image metadata
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            if img.get('src'):
                # Get image source URL
                src = img['src']
                alt = img.get('alt', '')
                
                # Resolve relative URLs
                abs_src = urljoin(base_url, src)
                
                # Add to images list
                images.append({
                    'url': abs_src,
                    'alt': alt,
                    'src': src
                })
                
                # We leave the URLs as they are for now
                # They will be rewritten later by the link manager
        
        return str(soup), images
    
    def convert_html_to_markdown(self, html_content: str, url: str) -> str:
        """
        Convert HTML content to Markdown.
        
        Args:
            html_content: Raw HTML content
            url: Original URL for resolving relative links
            
        Returns:
            Markdown content
        """
        # First, extract images
        processed_html, images = self.extract_images(html_content, url)
        
        # Convert to markdown
        markdown = self.h2t.handle(processed_html)
        
        # Rewrite links if a link map is provided
        if self.link_map:
            # Regular expression to find markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            
            def replace_link(match):
                text, link = match.groups()
                # Resolve relative URLs
                absolute_link = urljoin(url, link)
                
                # Replace with local link if in the map
                if absolute_link in self.link_map:
                    return f'[{text}]({self.link_map[absolute_link]})'
                return match.group(0)
            
            markdown = re.sub(link_pattern, replace_link, markdown)
        
        return markdown
    
    def add_front_matter(self, markdown: str, title: str, url: str) -> str:
        """
        Add front matter to the markdown file.
        
        Args:
            markdown: Markdown content
            title: Page title
            url: Original URL
            
        Returns:
            Markdown with front matter
        """
        front_matter = f"""---
title: "{title.replace('"', '\\"')}"
source_url: "{url}"
---

# {title}

[Source]({url})

"""
        return front_matter + markdown 