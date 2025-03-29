#!/usr/bin/env python3

"""
DocRepo Example Usage

This script demonstrates how to use DocRepo as a library in your own Python code.
"""

from docrepo import DocRepo

def main():
    """Example function showing DocRepo usage."""
    # Example 1: Basic usage
    print("Example 1: Basic usage with python.org")
    doc_repo = DocRepo(
        base_url="https://www.python.org/about/",
        output_dir="python_docs",
        max_depth=1,  # Only crawl the about page and its direct links
        delay=1.0     # Be extra nice with the delay
    )
    doc_repo.run()

    # Example 2: Using different options
    print("\nExample 2: Crawling a different site without downloading images")
    doc_repo = DocRepo(
        base_url="https://docs.python.org/3/tutorial/",
        output_dir="python_tutorial",
        max_depth=2,
        delay=0.75,
        download_images=False  # Skip image downloads
    )
    doc_repo.run()
    
    # Example 3: Ignoring robots.txt (use responsibly)
    print("\nExample 3: Crawling a site while ignoring robots.txt")
    doc_repo = DocRepo(
        base_url="https://example.com",
        output_dir="example_docs",
        max_depth=2,
        delay=1.0,  # Use a longer delay to be more respectful
        respect_robots_txt=False  # Ignore robots.txt restrictions
    )
    # Commented out to prevent actual execution in this example
    # doc_repo.run()
    print("Example 3 is commented out to prevent actual execution")
    print("Remove the comments to run this example")

if __name__ == "__main__":
    main() 