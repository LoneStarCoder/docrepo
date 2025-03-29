from setuptools import setup, find_packages
import os

# Read the contents of README.md file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="docrepo",
    version="0.1.0",
    description="Convert websites to Markdown documentation repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DocRepo Contributors",
    author_email="brodykilpatrick@gmail.com",
    url="https://github.com/LoneStarCoder/docrepo",
    packages=find_packages(include=["."]),
    py_modules=["docrepo", "crawler", "markdown_converter", "file_handler"],
    entry_points={
        "console_scripts": [
            "docrepo=docrepo:main",
        ],
    },
    install_requires=[
        "requests>=2.31.0,<3.0.0",
        "beautifulsoup4>=4.12.2,<5.0.0",
        "html2text>=2020.1.16,<2021.0.0",
        "urllib3>=2.0.7,<3.0.0",
        "tqdm>=4.66.1,<5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    keywords="documentation, web scraping, markdown, html, converter",
    python_requires=">=3.7",
    license="MIT",
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/LoneStarCoder/docrepo/issues",
        "Source": "https://github.com/LoneStarCoder/docrepo",
    },
) 