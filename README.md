# DocRepo - Website to Markdown Documentation Generator

![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange)

DocRepo is a Python application that crawls websites and converts them into a repository of interlinked Markdown files, making it easy to create offline documentation libraries from online resources.

## Features

- Crawls websites up to a specified depth
- Converts HTML pages to clean Markdown format
- Maintains the link structure between pages
- Downloads and stores images locally
- Creates an index page for easy navigation
- Respects robots.txt rules (with option to ignore)
- Rate limits requests to be a good web citizen

## Installation

### From PyPI (Recommended)

```bash
pip install docrepo
```

### From Source

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Usage

Basic usage:

```bash
python docrepo.py https://example.com
```

Or use the run.py script:

```bash
python run.py https://example.com
```

If installed via pip:

```bash
docrepo https://example.com
```

### Command Line Options

- `url`: The base URL to crawl (required)
- `-o, --output`: Output directory (default: `docrepo`)
- `-d, --depth`: Maximum depth to crawl (default: 3)
- `--delay`: Delay between requests in seconds (default: 0.5)
- `--no-images`: Skip downloading images (images will be linked to original URLs)
- `--ignore-robots`: Ignore robots.txt restrictions (use with caution)

Examples:

```bash
# Crawl with default settings
python docrepo.py https://python.org

# Specify output directory and maximum depth
python docrepo.py https://docs.python.org -o python_docs -d 2

# Use a longer delay between requests
python docrepo.py https://example.com --delay 1.0

# Skip downloading images
python docrepo.py https://example.com --no-images

# Ignore robots.txt restrictions (use responsibly)
python docrepo.py https://example.com --ignore-robots
```

## Generated Output

DocRepo creates a directory structure like this:

```
docrepo/
│
├── index.md                # Main index with links to all pages
├── example.com_index.md    # The home page
├── example.com_about.md    # Other pages
├── example.com_contact.md
│
└── images/                 # Downloaded images (if any)
    ├── logo.png
    └── ...
```

The Markdown files include:
- Front matter with metadata
- Page title and source link
- The page content in Markdown format
- Rewritten links to other local Markdown files
- Rewritten image links to local files (if image downloading is enabled)

## Using as a Library

You can also use DocRepo as a library in your own Python code:

```python
from docrepo import DocRepo

doc_repo = DocRepo(
    base_url="https://example.com",
    output_dir="my_docs",
    max_depth=2,
    delay=1.0,
    download_images=True,
    respect_robots_txt=True  # Set to False to ignore robots.txt
)
doc_repo.run()
```

For a complete example of using DocRepo as a library, see the included `example.py` file.

## Requirements

- Python 3.6+
- Required packages (see requirements.txt):
  - requests
  - beautifulsoup4
  - html2text
  - tqdm

## Troubleshooting

### Common Issues

**No content was crawled**
- Check that the URL is accessible in your browser
- Verify your internet connection
- The site might be blocking crawlers - try with `--ignore-robots`

**Error downloading images**
- Some sites protect images or load them via JavaScript
- Try with `--no-images` to skip image downloading

**Crawling is taking too long**
- Reduce the depth with `-d 1` or `-d 2`
- The site might have many links or slow response times

**Poor quality Markdown conversion**
- Some complex HTML layouts don't convert well to Markdown
- Consider manual editing of important pages

## Development

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies

```bash
git clone https://github.com/LoneStarCoder/docrepo.git
cd docrepo
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## Limitations

- JavaScript-rendered content won't be captured
- Some complex HTML layouts may not convert perfectly
- Very large websites may take significant time to crawl
- Image download might fail for some images with special protection

## License

MIT License

See the [LICENSE](LICENSE) file for details. 