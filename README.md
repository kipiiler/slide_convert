# Slide Converter

A Python-based tool for automatically scraping course slides from university websites and converting them into processed formats using the MinerU API. The tool can extract text, formulas, and tables from PDF slides with OCR capabilities.

## Features

- 🔍 **Automatic Slide Scraping**: Scrapes PDF slides from course schedule pages
- 📄 **PDF Processing**: Converts PDFs using MinerU API with OCR, formula, and table extraction
- 📋 **Single PDF Processing**: Process individual PDF files directly from URL
- 🤖 **AI-Powered Image Captioning**: Automatically generates accessible alt-text for images in markdown using LLM
- 💾 **State Management**: Tracks processing status and resumes from where it left off
- 📦 **Batch Processing**: Handles multiple slides efficiently with error recovery
- 🎯 **Flexible Filtering**: Filter slides by keywords to process only specific content
- 📊 **Progress Tracking**: Real-time status updates and comprehensive logging
- 🔄 **Resume Capability**: Continue processing from previous sessions

## Project Structure

```
slide_convert/
├── main.py                 # Main application entry point
├── slide_scraper.py        # Web scraping functionality for course slides
├── mineru_client.py        # MinerU API client for PDF processing
├── llm_client.py          # LLM integration for image captioning and analysis
├── zipper.py              # Download and extraction utilities
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── results/               # Processing results and state files
├── output/                # Downloaded and extracted content
└── scripts/               # Additional utility scripts
```

## Installation

### Prerequisites

- Python 3.7 or higher
- MinerU API token (get one from [mineru.net](https://mineru.net))
- Google API key for Gemini (optional, for image captioning)

### Setup

1. **Clone the repository** (or download the files):
   ```bash
   git clone <repository-url>
   cd slide_convert
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**:
   Create a `.env` file in the project root:
   ```env
   TOKEN=your_mineru_api_token_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Verify installation**:
   ```bash
   python main.py --help
   ```

## Usage

The tool offers multiple ways to run, from simple interactive mode to advanced command-line usage.

### Interactive Mode (Recommended for Beginners)

Run the tool interactively to be prompted for input:

```bash
python main.py --interactive
```

You'll be prompted to enter:
- Course schedule URL
- Keyword filter (optional)

### Command Line Usage

#### Basic Usage

Process all slides from a course:
```bash
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"
```

Process only slides containing "lecture":
```bash
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/" --keyword "lecture"
```

#### Single PDF Processing

Process a single PDF file directly:
```bash
python main.py --pdf-url "https://example.com/lecture01.pdf"
```

Process a single PDF with custom name:
```bash
python main.py --pdf-url "https://example.com/lecture01.pdf" --pdf-name "Introduction to Security"
```

Interactive mode for single PDF:
```bash
python main.py --pdf-interactive
```

#### Advanced Options

**Download only existing results** (no new processing):
```bash
python main.py --download-only
```

**Use custom results file**:
```bash
python main.py --url "https://example.com/course/" --results-file "my_results.json"
```

**Skip processing, only download**:
```bash
python main.py --skip-processing
```

### Command Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--url` | `-u` | Course schedule URL to scrape slides from |
| `--pdf-url` | | Direct PDF URL to process (single file mode) |
| `--pdf-name` | | Custom name for the PDF when using --pdf-url |
| `--keyword` | `-k` | Keyword to filter slides (e.g., "slides", "lecture") |
| `--interactive` | `-i` | Run in interactive mode (prompts for course URL input) |
| `--pdf-interactive` | | Run in interactive mode for single PDF processing |
| `--results-file` | `-r` | Path to results file (default: results/result.json) |
| `--download-only` | `-d` | Only download results for previously processed slides |
| `--skip-processing` | | Skip processing new slides, only download existing results |
| `--help` | `-h` | Show help message and exit |

## Examples

### Example 1: Process CSE Course Slides
```bash
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/" --keyword "slides"
```

### Example 2: Interactive Processing
```bash
python main.py --interactive
```
Then enter:
- URL: `https://courses.cs.washington.edu/courses/cse484/25sp/schedule/`
- Keyword: `slides` (or press Enter for all)

### Example 3: Process Single PDF
```bash
python main.py --pdf-url "https://cs.stanford.edu/~dabo/papers/sessionfixation.pdf"
```

### Example 4: Interactive Single PDF Processing
```bash
python main.py --pdf-interactive
```
Then enter:
- PDF URL: `https://example.com/lecture01.pdf`
- Custom name: `Security Fundamentals` (or press Enter to auto-generate)

### Example 5: Resume Previous Session
```bash
python main.py --download-only
```

## AI-Powered Image Captioning

The tool includes advanced LLM integration for automatically generating accessible alt-text for images in markdown files. This feature uses Google's Gemini AI to analyze images from lecture slides and create meaningful descriptions.

### Features

- **Automatic Alt-Text Generation**: Analyzes images and generates descriptive captions
- **Accessibility Focused**: Creates captions specifically designed for screen readers
- **Batch Processing**: Processes all images in extracted slide directories
- **Rate Limiting**: Built-in rate limiting to respect API quotas
- **Smart Skipping**: Only processes images without existing alt-text

### Setup for Image Captioning

1. **Get Google API Key**:
   - Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file as `GOOGLE_API_KEY`

2. **Configure Environment**:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### Usage

#### Automatic Processing
After running the main slide conversion, you can automatically caption all images:

```bash
python llm_client.py
```

This will:
- Process all directories in the `output/` folder
- Analyze images without alt-text
- Generate accessibility-focused captions
- Create new markdown files with `captioned.md` suffix

#### Manual Processing
You can also use the image captioning as a standalone tool:

```python
from llm_client import GeminiClient, ImageCaptionAgent

# Initialize the LLM client
llm_client = GeminiClient()
agent = ImageCaptionAgent(llm_client)

# Process a specific directory
agent.process_directory("output/lecture01-slides.pdf")
```

### Image Captioning Configuration

#### LLM Settings
- **Model**: Uses `gemini-2.0-flash-lite` by default
- **Rate Limit**: 30 requests per minute (configurable)
- **Prompt**: Optimized for computer security lecture content

#### Customizing the Caption Prompt
You can modify the prompt in `llm_client.py`:

```python
self.image_prompt = """
Your custom prompt for generating image captions.
Focus on accessibility and educational content.
"""
```

### Example Output

**Before (no alt-text):**
```markdown
![](images/diagram-01.png)
```

**After (with AI-generated caption):**
```markdown
![Network security architecture diagram showing firewall placement between internal and external networks](images/diagram-01.png)
```

### Advanced Features

#### Rate Limiting
The system automatically handles API rate limits:
- Tracks requests per minute
- Automatically waits when limits are reached
- Provides progress feedback

#### Error Handling
- Gracefully handles missing images
- Continues processing if individual images fail
- Provides detailed error messages

#### Batch Processing
Process multiple slide sets efficiently:
```python
# Process all output directories
for directory in os.listdir("output/"):
    if os.path.isdir(f"output/{directory}"):
        agent.process_directory(f"output/{directory}")
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: MinerU API token
TOKEN=your_mineru_api_token_here

# Optional: Google API key for image captioning
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Additional configuration can be added here
```

### Processing Options

The tool automatically configures PDF processing with:
- **OCR**: Enabled for text extraction from images
- **Formula Detection**: Enabled for mathematical content
- **Table Extraction**: Enabled for structured data
- **Language**: English (configurable in code)

## Output

### Results Structure

Processed results are saved in:
- `results/result.json`: Processing status and metadata
- `output/`: Extracted content organized by slide name

### Processing States

- **pending**: Task created, waiting to start
- **running**: Currently being processed
- **converting**: Converting to final format
- **done**: Successfully completed
- **failed**: Processing failed with error

## Troubleshooting

### Common Issues

1. **"TOKEN environment variable not found"**
   - Create a `.env` file with your MinerU API token
   - Ensure the file is in the project root directory

2. **"GOOGLE_API_KEY not found in .env file"**
   - Add your Google API key to the `.env` file
   - Ensure you have access to the Gemini API
   - Check that your API key has proper permissions

3. **"No slides found matching the criteria"**
   - Check if the URL is correct and accessible
   - Try without a keyword filter first
   - Verify the website structure hasn't changed

4. **Processing fails or times out**
   - Check your internet connection
   - Verify your API token is valid and has credits
   - Use `--download-only` to retrieve partial results

5. **Image captioning fails**
   - Verify your Google API key is valid
   - Check that you have Gemini API access
   - Ensure images exist in the specified paths
   - Check rate limiting if processing many images

6. **Permission errors on Windows**
   - Run PowerShell/Command Prompt as Administrator
   - Check file permissions in the project directory

### Debug Mode

For detailed logging, you can modify the scripts or add print statements to see what's happening during processing.

## Dependencies

- `requests`: HTTP requests for web scraping and API calls
- `beautifulsoup4`: HTML parsing for slide extraction
- `python-dotenv`: Environment variable management
- `google-generativeai`: Google Gemini AI for image analysis
- `pillow`: Image processing capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational purposes. Make sure to comply with the terms of service of any websites you scrape and APIs you use.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are installed correctly
4. Verify your API credentials are valid

## Changelog

### Current Version
- Added command-line argument support
- Implemented interactive mode
- Added state management and resume capability
- Improved error handling and recovery
- Added AI-powered image captioning with Google Gemini
- Implemented rate limiting for LLM API calls
- Added accessibility-focused alt-text generation
- Added comprehensive documentation 