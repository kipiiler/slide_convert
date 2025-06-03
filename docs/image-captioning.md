# AI-Powered Image Captioning Guide

The Slide Converter includes advanced AI integration for automatically generating accessible alt-text for images in markdown files using Google's Gemini AI.

## Overview

This feature analyzes images from processed slides and creates meaningful descriptions specifically designed for accessibility and screen readers. It's particularly valuable for educational content where visual elements are crucial for understanding.

## Features

- **Automatic Alt-Text Generation**: Analyzes images and generates descriptive captions
- **Accessibility Focused**: Creates captions specifically designed for screen readers
- **Batch Processing**: Processes all images in extracted slide directories
- **Rate Limiting**: Built-in rate limiting to respect API quotas
- **Smart Skipping**: Only processes images without existing alt-text
- **Educational Content Optimized**: Prompts tuned for academic and lecture content

## Setup

### Prerequisites

1. **Google API Key**: Required for Gemini AI access
2. **Processed Slides**: Images must be extracted from slides first
3. **Environment Configuration**: API key in `.env` file

### Getting Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign up or log in to your Google account
3. Create a new API key
4. Ensure you have access to the Gemini API
5. Add the key to your `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Verify Setup

Test that the AI client works:

```bash
# This will show an error if the API key is missing or invalid
python llm_client.py
```

## Usage

### Automatic Processing

After running slide conversion, automatically caption all images:

```bash
python llm_client.py
```

This will:
1. Scan all directories in the `output/` folder
2. Find markdown files with images
3. Analyze images that don't have alt-text
4. Generate accessibility-focused captions
5. Create new markdown files with `captioned.md` suffix

### Manual Processing

Process a specific output directory:

```python
from llm_client import GeminiClient, ImageCaptionAgent

# Initialize the LLM client
llm_client = GeminiClient()
agent = ImageCaptionAgent(llm_client)

# Process a specific directory
agent.process_directory("output/lecture01-slides.pdf")
```

### Integration with Main Tool

The image captioning works seamlessly with the main tool:

1. **Process slides first**:
   ```bash
   python main.py --url "https://example.com/course/"
   ```

2. **Then generate captions**:
   ```bash
   python llm_client.py
   ```

## Configuration

### LLM Settings

Default configuration uses:
- **Model**: `gemini-2.0-flash-lite`
- **Rate Limit**: 30 requests per minute
- **Language**: English
- **Prompt**: Optimized for computer security lecture content

### Customizing the Model

Modify the model in `llm_client.py`:

```python
class GeminiClient(LLMClient):
    def __init__(self, model_name: str = 'gemini-2.0-flash-lite', rate_limit: int = 30):
        # Change model_name to use different Gemini model
        # Change rate_limit for different API quotas
```

### Customizing the Caption Prompt

The prompt is optimized for educational content but can be customized:

```python
class ImageCaptionAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.image_prompt = """
        Analyze this image from a computer security lecture slide. 
        Write a short and concise caption for the image that is use for accessibility (alt text for image).

        Give back only the caption, no other text, no markdown formatting, no code block, no code, no nothing.
        """
```

**Customization Examples:**

For mathematics content:
```python
self.image_prompt = """
Analyze this mathematical diagram or equation. Create a brief, accessible description 
for screen readers that explains the key mathematical concepts shown.

Provide only the description, no additional formatting.
"""
```

For general academic content:
```python
self.image_prompt = """
Describe this academic slide image for accessibility purposes. Focus on the main 
educational concepts, diagrams, or data presented.

Return only the descriptive caption.
"""
```

## Output Examples

### Before Processing

```markdown
![](images/diagram-01.png)
![](images/chart-02.png)
![](images/code-example-03.png)
```

### After AI Captioning

```markdown
![Network security architecture diagram showing firewall placement between internal and external networks](images/diagram-01.png)
![Bar chart comparing encryption algorithm performance with AES-256 showing highest throughput](images/chart-02.png)
![Python code example demonstrating secure password hashing using bcrypt library](images/code-example-03.png)
```

## Rate Limiting and Performance

### Understanding Rate Limits

The system automatically handles API rate limits:
- **Default**: 30 requests per minute
- **Automatic waiting**: Pauses when limit reached
- **Progress feedback**: Shows wait times
- **Resumable**: Can be interrupted and resumed

### Managing Large Batches

For processing many images:

1. **Monitor progress**:
   ```bash
   python llm_client.py
   # Watch for rate limiting messages
   ```

2. **Adjust rate limits** if you have higher quotas:
   ```python
   # In llm_client.py
   llm_client = GeminiClient(rate_limit=60)  # 60 requests per minute
   ```

3. **Process in chunks** for very large datasets:
   ```python
   # Process specific directories one at a time
   agent.process_directory("output/lecture01-slides.pdf")
   # Wait if needed, then process next
   agent.process_directory("output/lecture02-slides.pdf")
   ```

## Advanced Features

### Batch Processing All Outputs

The default behavior processes all output directories:

```python
def main():
    llm_client = GeminiClient()
    agent = ImageCaptionAgent(llm_client)

    dirs = "output/"
    for dir in os.listdir(dirs):
        directory_path = os.path.join(dirs, dir)
        if os.path.isdir(directory_path):
            agent.process_directory(directory_path)
```

### Selective Processing

Process only specific files or patterns:

```python
import os
from llm_client import GeminiClient, ImageCaptionAgent

llm_client = GeminiClient()
agent = ImageCaptionAgent(llm_client)

# Process only lecture slides (not assignments)
for dirname in os.listdir("output/"):
    if "lecture" in dirname.lower():
        agent.process_directory(f"output/{dirname}")
```

### Error Handling

The system gracefully handles:
- **Missing images**: Skips and continues with next
- **API errors**: Logs error and continues
- **File permission issues**: Reports and continues
- **Network problems**: Retries with backoff

## File Organization

### Input Structure

The captioning tool expects this structure:
```
output/
├── lecture01-slides.pdf/
│   ├── full.md              # Original markdown
│   └── images/
│       ├── image_001.png
│       └── image_002.png
└── lecture02-slides.pdf/
    └── ...
```

### Output Structure

After captioning:
```
output/
├── lecture01-slides.pdf/
│   ├── full.md              # Original markdown
│   ├── captioned.md         # New file with captions
│   └── images/
│       ├── image_001.png
│       └── image_002.png
└── lecture02-slides.pdf/
    └── ...
```

## Quality and Accuracy

### Caption Quality

The AI generates captions optimized for:
- **Educational context**: Understands academic content
- **Accessibility standards**: Follows alt-text best practices
- **Conciseness**: Brief but descriptive
- **Technical accuracy**: Recognizes common academic diagrams

### Manual Review

While the AI generates high-quality captions, consider reviewing for:
- **Technical terminology**: Verify correct academic terms
- **Context specificity**: Ensure relevance to your subject matter
- **Length appropriateness**: Adjust if too verbose or brief

### Improving Results

For better captions:
1. **Use high-quality slide images**: Clear diagrams produce better descriptions
2. **Customize prompts**: Tailor to your specific academic domain
3. **Process iteratively**: Review and refine prompt based on results

## Troubleshooting

### Common Issues

**"GOOGLE_API_KEY not found in .env file"**
- Ensure `.env` file exists in project root
- Verify the API key is correctly formatted
- Check for extra spaces or quotes

**Rate limiting errors**
- Wait for the automatic retry
- Reduce rate limit in configuration
- Process smaller batches

**Poor caption quality**
- Customize the prompt for your content type
- Ensure images are clear and high-resolution
- Review and adjust prompt iteratively

**Permission errors**
- Ensure output directories are writable
- Close any programs accessing the files
- Run with appropriate permissions

### Debug Mode

Add debugging to see what's happening:

```python
# In llm_client.py, add print statements
def analyze_image(self, image_path: str, prompt: str) -> Optional[str]:
    print(f"Processing: {image_path}")
    # ... existing code
    print(f"Generated caption: {response.text}")
```

## Integration Workflow

### Complete Processing Pipeline

1. **Process slides**:
   ```bash
   python main.py --url "https://example.com/course/" --keyword "lecture"
   ```

2. **Generate captions**:
   ```bash
   python llm_client.py
   ```

3. **Review results**:
   ```bash
   # Check captioned.md files in output directories
   ls output/*/captioned.md
   ```

4. **Clean up if needed**:
   ```bash
   python main.py --cache-interactive
   ```

### Automation Scripts

For regular processing, create a script:

```bash
#!/bin/bash
# process_and_caption.sh

echo "Processing slides..."
python main.py --url "$1" --keyword "lecture"

echo "Generating captions..."
python llm_client.py

echo "Complete! Check output directories for captioned.md files"
```

Usage:
```bash
chmod +x process_and_caption.sh
./process_and_caption.sh "https://course.edu/schedule/"
```

## Best Practices

1. **Process slides first**: Always extract content before captioning
2. **Review API usage**: Monitor your Google API quota
3. **Customize prompts**: Tailor to your specific academic domain
4. **Batch processing**: Process multiple courses together for efficiency
5. **Quality review**: Spot-check generated captions for accuracy
6. **Backup originals**: Keep original markdown files before captioning

For more information on integrating image captioning with your workflow, see the [Usage Guide](usage.md). 