# Installation Guide

This guide covers everything you need to get the Slide Converter up and running.

## Prerequisites

- **Python 3.7 or higher**
- **MinerU API token** - Get one from [mineru.net](https://mineru.net)
- **Google API key** (optional) - For AI image captioning from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Setup Steps

### 1. Clone or Download

Clone the repository (or download the files):
```bash
git clone <repository-url>
cd slide_convert
```

### 2. Install Dependencies

Install all required Python packages:
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `requests` - HTTP requests for web scraping and API calls
- `beautifulsoup4` - HTML parsing for slide extraction
- `python-dotenv` - Environment variable management
- `google-generativeai` - Google Gemini AI for image analysis
- `pillow` - Image processing capabilities

### 3. Environment Configuration

Create a `.env` file in the project root directory:

```env
# Required: MinerU API token
TOKEN=your_mineru_api_token_here

# Optional: Google API key for image captioning
GOOGLE_API_KEY=your_google_api_key_here
```

**Getting API Keys:**

#### MinerU API Token
1. Visit [mineru.net](https://mineru.net)
2. Sign up or log in to your account
3. Navigate to API settings
4. Generate a new API token
5. Copy the token to your `.env` file

#### Google API Key (Optional)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Ensure you have access to the Gemini API
4. Add the key to your `.env` file

### 4. Verify Installation

Test that everything is working correctly:

```bash
# Check command line help
python main.py --help

# Test basic functionality (should show cache list, even if empty)
python main.py --cache-list
```

## Directory Structure

After installation, your project should look like this:

```
slide_convert/
├── main.py                 # Main application entry point
├── slide_scraper.py        # Web scraping functionality
├── mineru_client.py        # MinerU API client
├── llm_client.py          # LLM integration for image captioning
├── zipper.py              # Download and extraction utilities
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (you create this)
├── docs/                  # Documentation files
├── results/               # Processing results (created automatically)
└── output/                # Downloaded content (created automatically)
```

## Troubleshooting Installation

### Common Issues

**"TOKEN environment variable not found"**
- Ensure you created the `.env` file in the correct directory
- Check that the file contains `TOKEN=your_actual_token`
- Verify there are no extra spaces around the equals sign

**"Module not found" errors**
- Run `pip install -r requirements.txt` again
- Consider using a virtual environment:
  ```bash
  python -m venv env
  source env/bin/activate  # On Windows: env\Scripts\activate
  pip install -r requirements.txt
  ```

**Permission errors**
- On Windows, run PowerShell as Administrator
- On macOS/Linux, check file permissions with `ls -la`

**Python version issues**
- Check your Python version: `python --version`
- Ensure you're using Python 3.7 or higher
- You may need to use `python3` instead of `python`

### Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

```bash
# Create virtual environment
python -m venv slide_converter_env

# Activate virtual environment
# On Windows:
slide_converter_env\Scripts\activate
# On macOS/Linux:
source slide_converter_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

## Next Steps

Once installation is complete, check out:
- [Quick Start Guide](../README.md#quick-start) - Get started immediately
- [Usage Guide](usage.md) - Detailed usage instructions
- [Configuration Guide](configuration.md) - Advanced configuration options 