# Usage Guide

This guide covers all the ways to use the Slide Converter tool, from basic course scraping to advanced single PDF processing and local file processing.

## Overview

The Slide Converter offers four main modes of operation:
1. **Course Scraping** - Extract slides from course websites
2. **Single PDF Processing** - Process individual PDF files from URLs
3. **Local File Processing** - Process PDF files stored locally on your computer
4. **Cache Management** - Manage processed files

## Course Scraping Mode

### Interactive Mode (Recommended for Beginners)

The easiest way to get started:

```bash
python main.py --interactive
```

You'll be prompted to enter:
- **Course schedule URL**: The webpage containing slide links
- **Keyword filter**: Optional filter to match specific slides

**Example Session:**
```
=== Slide Converter Setup ===
Enter the course schedule URL: https://courses.cs.washington.edu/courses/cse484/25sp/schedule/
Enter keyword to filter slides (or press Enter to process all slides): slides
```

### Command Line Mode

For automation and scripting:

```bash
# Process all slides from a course
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"

# Process only slides containing "lecture"
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/" --keyword "lecture"

# Use custom results file
python main.py --url "https://example.com/course/" --results-file "custom_results.json"
```

### How Course Scraping Works

1. **Web Scraping**: The tool visits the course URL and finds all PDF links
2. **Filtering**: Applies keyword filters if specified
3. **Name Processing**: Extracts clean names from PDF URLs
4. **Duplicate Detection**: Skips already processed files
5. **Batch Processing**: Processes all new slides sequentially
6. **State Management**: Saves progress after each file
7. **Download**: Automatically downloads and extracts results

## Single PDF Processing

### Direct URL Processing

Process individual PDF files directly:

```bash
# Basic single PDF processing
python main.py --pdf-url "https://example.com/lecture01.pdf"

# With custom name
python main.py --pdf-url "https://example.com/lecture01.pdf" --pdf-name "Introduction to Security"
```

### Interactive PDF Mode

For manual input:

```bash
python main.py --pdf-interactive
```

**Example Session:**
```
=== Single PDF Processing Setup ===
Enter the PDF URL: https://cs.stanford.edu/~dabo/papers/sessionfixation.pdf
Enter custom name for the PDF (or press Enter to auto-generate): Session Fixation Paper
```

### PDF Name Handling

The tool automatically handles PDF naming:
- **Auto-generation**: Extracts filename from URL
- **Custom names**: Use `--pdf-name` or interactive input
- **Extension handling**: Automatically adds `.pdf` extension if missing
- **Timestamp fallback**: Uses timestamp if name cannot be extracted

## Local File Processing

Process PDF files stored on your local computer without needing to upload them to external URLs first.

### Direct Local File Processing

Process local PDF files directly:

```bash
# Basic local file processing
python main.py --local-file "document.pdf"
python main.py --local-file "/path/to/research_paper.pdf"

# With custom name
python main.py --local-file "document.pdf" --local-name "Chapter 1 Introduction"
```

### Interactive Local File Mode

For manual input and easier file selection:

```bash
python main.py --local-interactive
```

**Example Session:**
```
=== Local File Processing Setup ===
Enter the path to the local PDF file: C:\Users\Documents\lecture01.pdf
Enter custom name for the file (or press Enter to auto-generate): Security Fundamentals
```

### Local File Benefits

Local file processing offers several advantages:
- **No public URL required** - Files stay on your machine during initial processing
- **Privacy** - Sensitive documents don't need to be shared via public URLs
- **Large files** - Better handling of large files without URL timeout issues
- **Batch local processing** - Process multiple local files efficiently

### File Path Handling

The tool supports various file path formats:
- **Relative paths**: `document.pdf`, `papers/research.pdf`
- **Absolute paths**: `/home/user/docs/file.pdf`, `C:\Users\Documents\file.pdf`
- **File validation**: Automatically checks if file exists before processing

### Local File Name Management

Similar to PDF URL processing, the tool handles naming automatically:
- **Auto-generation**: Uses the filename if no custom name provided
- **Custom names**: Use `--local-name` or interactive input
- **Extension handling**: Automatically ensures `.pdf` extension
- **Path extraction**: Extracts just the filename from full paths

### How Local File Processing Works

1. **File Upload**: Securely uploads file to MinerU's processing servers
2. **Processing**: Uses the same OCR, formula, and table extraction as URL-based processing
3. **Results**: Downloads processed results back to your local machine
4. **Cleanup**: Files are automatically removed from servers after processing

## Advanced Usage Patterns

### Resume Operations

Download results from previous processing sessions:

```bash
# Download only existing results (no new processing)
python main.py --download-only

# Skip processing, only download
python main.py --skip-processing
```

### Custom Configuration

Use different results files for different projects:

```bash
# Use custom results file
python main.py --url "https://example.com/" --results-file "project1_results.json"

# Process with different configuration
python main.py --pdf-url "https://example.com/doc.pdf" --results-file "single_docs.json"
```

### Batch Operations

Process multiple courses or documents efficiently:

```bash
# Process multiple courses (run separately)
python main.py --url "https://course1.edu/schedule/" --results-file "course1.json"
python main.py --url "https://course2.edu/schedule/" --results-file "course2.json"

# Resume all downloads
python main.py --download-only --results-file "course1.json"
python main.py --download-only --results-file "course2.json"
```

### Local File Operations

Process multiple local files with different configurations:

```bash
# Process different types of documents
python main.py --local-file "lecture.pdf" --local-name "Course Lecture" --results-file "course.json"
python main.py --local-file "paper.pdf" --local-name "Research Paper" --results-file "research.json"

# Resume downloads for local files
python main.py --download-only --results-file "course.json"
```

## Processing Options

### OCR and Content Extraction

All processing modes (course, PDF URL, local file) include:
- **OCR**: Optical Character Recognition for scanned text
- **Formula Detection**: Mathematical equations and formulas
- **Table Extraction**: Structured data from tables
- **Image Extraction**: All images with metadata

### Upload vs Local Processing

**Local File Processing Benefits:**
- Files are securely uploaded to MinerU's servers for processing
- Processing happens with the same full capabilities as URL-based processing
- Files are automatically cleaned up from servers after processing
- Results are downloaded back to your local machine

**Comparison:**

| Feature | URL Processing | Local File Processing |
|---------|----------------|----------------------|
| File location | Must be publicly accessible | Can be anywhere on your computer |
| Privacy | URL must be shareable | File stays local until secure upload |
| File size limits | Limited by URL accessibility | Limited by upload size (200MB max) |
| Processing speed | Depends on URL availability | Depends on upload speed |
| Security | URL-based access | Secure temporary upload |

### Language Support

Default language is English, but can be configured in the code:
```python
# In main.py, modify the create_task calls
task_id = client.create_task(
    url=slide['url'],
    name=slide['name'],
    is_ocr=True,
    enable_formula=True,
    enable_table=True,
    language='en'  # Change to your preferred language
)
```

## Error Handling

### Graceful Recovery

The tool handles errors gracefully:
- **Network issues**: Retries with backoff
- **Individual failures**: Continues with remaining files
- **State preservation**: Saves progress before each operation
- **Resume capability**: Can restart from where it left off

### Common Error Scenarios

**Website access issues:**
```bash
# If scraping fails, try with different keyword
python main.py --url "https://example.com/" --keyword "pdf"
```

**PDF processing failures:**
```bash
# Check results and retry failed items
python main.py --cache-list
python main.py --download-only
```

## Output Structure

### Results Organization

Processed files are organized as:

```
output/
├── lecture01-slides.pdf/
│   ├── full.md              # Complete markdown
│   ├── images/              # Extracted images
│   │   ├── image_001.png
│   │   └── image_002.png
│   └── metadata.json       # Processing metadata
├── lecture02-crypto.pdf/
│   └── ...
└── ...
```

### State Management

Processing state is tracked in:
- `results/result.json` - Default results file
- Custom files via `--results-file` option

Each entry contains:
- Processing state (pending, running, done, failed)
- Original URL and file name
- Creation timestamp
- Error messages (if any)
- Download URLs (when complete)

## Best Practices

### Efficient Processing

1. **Use keywords** to filter only needed slides
2. **Check cache** before reprocessing with `--cache-list`
3. **Resume downloads** using `--download-only`
4. **Use custom results files** for different projects

### Resource Management

1. **Monitor API usage** - MinerU has usage limits
2. **Clean up cache** regularly with cache management tools
3. **Use appropriate keywords** to avoid processing unwanted files

### Workflow Recommendations

1. **Start with interactive mode** to test URLs
2. **Use command line** for automation
3. **Check results** with `--cache-list`
4. **Clean up** with cache management when done

## Next Steps

- [Cache Management Guide](cache-management.md) - Manage processed files
- [Image Captioning Guide](image-captioning.md) - AI-powered accessibility features
- [Configuration Guide](configuration.md) - Advanced configuration options
- [API Reference](api-reference.md) - Complete command reference 