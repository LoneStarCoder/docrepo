import os
import re
import unicodedata
import requests
from urllib.parse import urlparse
from typing import Dict, List, Set


class FileHandler:
    def __init__(self, output_dir: str = "docrepo"):
        """
        Initialize the file handler.
        
        Args:
            output_dir: Directory where the Markdown files will be saved
        """
        self.output_dir = output_dir
        self.ensure_directory(self.output_dir)
        
        # For tracking created files and avoiding duplicates
        self.created_files: Set[str] = set()
        self.url_to_file_map: Dict[str, str] = {}
    
    def ensure_directory(self, directory: str) -> None:
        """Create directory if it doesn't exist."""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def sanitize_filename(self, url: str) -> str:
        """
        Convert a URL into a valid filename.
        
        Args:
            url: The URL to convert
            
        Returns:
            A sanitized filename
        """
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Start with the hostname
        filename = parsed_url.netloc
        
        # Add the path, but remove trailing slashes
        path = parsed_url.path.rstrip('/')
        if path:
            # Replace slashes with underscores
            path = path.replace('/', '_')
            filename += path
        
        # If the URL has no path, add an underscore to avoid filename collision
        if not path and not parsed_url.query:
            filename += '_index'
        
        # Add query parameters if present
        if parsed_url.query:
            filename += '_' + parsed_url.query.replace('&', '_').replace('=', '-')
        
        # Remove invalid filename characters
        filename = re.sub(r'[^\w\-\.]', '_', filename)
        
        # Normalize unicode characters
        filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
        
        # Ensure filename isn't too long
        if len(filename) > 200:
            # Keep the first 100 and last 95 characters
            filename = filename[:100] + '_' + filename[-95:]
        
        # Add markdown extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        return filename
    
    def generate_unique_filename(self, url: str) -> str:
        """
        Generate a unique filename based on the URL.
        
        Args:
            url: The URL to convert to a filename
            
        Returns:
            A unique filename for the URL
        """
        base_filename = self.sanitize_filename(url)
        filename = base_filename
        counter = 1
        
        # If the filename already exists, append a counter
        while filename in self.created_files:
            # Split the name and extension
            name, ext = os.path.splitext(base_filename)
            filename = f"{name}_{counter}{ext}"
            counter += 1
        
        self.created_files.add(filename)
        self.url_to_file_map[url] = filename
        return filename
    
    def save_markdown(self, url: str, markdown_content: str) -> str:
        """
        Save markdown content to a file.
        
        Args:
            url: Original URL
            markdown_content: Markdown content to save
            
        Returns:
            Path to the saved file
        """
        filename = self.generate_unique_filename(url)
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return filename
    
    def download_image(self, image_url: str, dirname: str = "images") -> str:
        """
        Download an image and save it locally.
        
        Args:
            image_url: URL of the image
            dirname: Directory to save images
            
        Returns:
            Local path to the image
        """
        images_dir = os.path.join(self.output_dir, dirname)
        self.ensure_directory(images_dir)
        
        # Generate filename from URL
        parsed_url = urlparse(image_url)
        path = parsed_url.path
        
        # Get the original filename from the URL
        original_filename = os.path.basename(path)
        
        # Remove query parameters
        original_filename = original_filename.split('?')[0]
        
        # If no filename was found, use a default
        if not original_filename:
            original_filename = f"image_{len(self.created_files)}.jpg"
        
        # Sanitize the filename
        filename = re.sub(r'[^\w\-\.]', '_', original_filename)
        
        # Ensure unique filename
        counter = 1
        unique_filename = filename
        while os.path.join(images_dir, unique_filename) in self.created_files:
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{counter}{ext}"
            counter += 1
        
        filepath = os.path.join(images_dir, unique_filename)
        self.created_files.add(filepath)
        
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return os.path.join(dirname, unique_filename)
        
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")
            return image_url  # Return original URL on failure
    
    def create_index(self, url_title_map: Dict[str, str]) -> str:
        """
        Create an index file with links to all downloaded pages.
        
        Args:
            url_title_map: Dictionary mapping URLs to page titles
            
        Returns:
            Path to the index file
        """
        index_content = "# Documentation Repository Index\n\n"
        
        # Sort by title for better organization
        sorted_urls = sorted(url_title_map.items(), key=lambda x: x[1])
        
        for url, title in sorted_urls:
            if url in self.url_to_file_map:
                filename = self.url_to_file_map[url]
                index_content += f"- [{title}]({filename})\n"
        
        # Save the index file
        with open(os.path.join(self.output_dir, "index.md"), 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return "index.md" 