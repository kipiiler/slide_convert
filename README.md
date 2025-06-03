# Slide Converter

A Python tool for automatically scraping course slides and converting them to processed formats using AI-powered OCR, with intelligent image captioning for accessibility.

## ✨ Features

- 🔍 **Automatic Slide Scraping** - Extract slides from course websites
- 📄 **AI-Powered PDF Processing** - OCR, formula detection, and table extraction
- 📋 **Single PDF Processing** - Process individual files directly
- 💻 **Local File Processing** - Process PDF files stored on your computer
- 🤖 **Image Captioning** - AI-generated alt-text for accessibility
- 🗂️ **Cache Management** - Organize and clean processed files
- 💾 **State Management** - Resume interrupted processing

## 🚀 Quick Start

### 1. Installation

```bash
# Clone and install
git clone <repository-url>
cd slide_convert
pip install -r requirements.txt

# Create environment file
echo "TOKEN=your_mineru_api_token" > .env
```

### 2. Basic Usage

**Interactive Mode (Recommended):**
```bash
python main.py --interactive
```

**Process Course Slides:**
```bash
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"
```

**Process Single PDF:**
```bash
python main.py --pdf-url "https://example.com/lecture.pdf"
```

**Process Local File:**
```bash
python main.py --local-file "document.pdf" --local-name "My Document"
```

### 3. Manage Results

```bash
# List processed files
python main.py --cache-list

# Download results
python main.py --download-only

# Clean up cache
python main.py --cache-interactive
```

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [Installation Guide](docs/installation.md) | Complete setup instructions and troubleshooting |
| [Usage Guide](docs/usage.md) | Detailed usage patterns and workflows |
| [Cache Management](docs/cache-management.md) | File management and cleanup |
| [Image Captioning](docs/image-captioning.md) | AI-powered accessibility features |
| [API Reference](docs/api-reference.md) | Complete command-line reference |

## ⚡ Examples

**Course Processing:**
```bash
# Interactive setup
python main.py --interactive

# Command line with filtering
python main.py --url "https://university.edu/schedule/" --keyword "lecture"
```

**Single Documents:**
```bash
# Direct PDF processing
python main.py --pdf-url "https://arxiv.org/pdf/paper.pdf" --pdf-name "Research Paper"

# Interactive PDF mode
python main.py --pdf-interactive

# Local file processing
python main.py --local-file "document.pdf" --local-name "My Document"

# Interactive local file mode
python main.py --local-interactive
```

**Maintenance:**
```bash
# View cache
python main.py --cache-list

# Interactive cleanup
python main.py --cache-interactive
```

## 🔧 Configuration

Create a `.env` file with your API tokens:

```env
# Required: MinerU API token
TOKEN=your_mineru_token_here

# Optional: Google API key for image captioning
GOOGLE_API_KEY=your_google_api_key_here
```

**Get API Keys:**
- **MinerU**: [mineru.net](https://mineru.net) - PDF processing
- **Google AI**: [Google AI Studio](https://makersuite.google.com/app/apikey) - Image captioning

## 📁 Output Structure

```
output/
├── lecture01-slides.pdf/
│   ├── full.md              # Extracted content
│   ├── captioned.md         # With AI alt-text
│   └── images/              # Extracted images
└── results/
    └── result.json          # Processing state
```

## 🔗 Key Features

### Course Scraping
- Automatically finds PDF links on course pages
- Keyword filtering for specific content
- Batch processing with error recovery

### PDF Processing
- OCR for scanned documents
- Formula and table extraction
- Image extraction with metadata
- Supports both URL-based and local file processing

### Local File Processing
- Process files stored on your computer
- Secure temporary upload to processing servers
- No need for public URLs or file sharing
- Full OCR and content extraction capabilities

### AI Image Captioning
- Accessibility-focused descriptions
- Educational content optimization
- Batch processing with rate limiting

### Cache Management
- Interactive file selection
- Storage usage tracking
- Selective cleanup options

## 🛠️ Requirements

- Python 3.7+
- MinerU API token ([Get one here](https://mineru.net))
- Google API key (optional, for image captioning)

## 📋 Command Reference

| Command | Purpose |
|---------|---------|
| `--interactive` | Interactive course processing |
| `--pdf-interactive` | Interactive single PDF processing |
| `--local-interactive` | Interactive local file processing |
| `--cache-list` | List all processed files |
| `--cache-interactive` | Interactive cache management |
| `--download-only` | Download existing results |
| `--help` | Show all options |

## 🤝 Getting Help

1. **Quick Issues**: Check the [Installation Guide](docs/installation.md#troubleshooting-installation)
2. **Usage Questions**: See the [Usage Guide](docs/usage.md)
3. **Cache Problems**: Read [Cache Management](docs/cache-management.md)
4. **AI Features**: Check [Image Captioning Guide](docs/image-captioning.md)
5. **Complete Reference**: Use the [API Reference](docs/api-reference.md)

## 📄 License

This project is provided as-is for educational purposes. Please comply with the terms of service of any websites you scrape and APIs you use.

---

**Start here:** Run `python main.py --interactive` for guided setup, or check the [Installation Guide](docs/installation.md) for detailed setup instructions. 