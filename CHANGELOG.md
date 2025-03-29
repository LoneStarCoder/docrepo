# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-03-28

### Added
- Initial release
- Web crawling functionality with depth control
- HTML to Markdown conversion
- Link rewriting to maintain references between documents
- Image downloading capability
- robots.txt compliance (with option to ignore)
- Index page generation
- Command-line interface
- Library API for programmatic use

### Known Issues
- No support for JavaScript-rendered content
- Complex HTML layouts may not convert perfectly to Markdown
- Image download might fail for some images with protection
- Large websites may take significant time to crawl 