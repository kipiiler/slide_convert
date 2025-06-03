# API Reference

Complete command-line reference for the Slide Converter tool.

## Command Syntax

```bash
python main.py [OPTIONS]
```

## Global Options

### Core Processing Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--url` | `-u` | string | Course schedule URL to scrape slides from |
| `--pdf-url` | | string | Direct PDF URL to process (single file mode) |
| `--pdf-name` | | string | Custom name for the PDF when using --pdf-url |
| `--keyword` | `-k` | string | Keyword to filter slides (e.g., "slides", "lecture") |

### Interactive Modes

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--interactive` | `-i` | flag | Run in interactive mode (prompts for course URL input) |
| `--pdf-interactive` | | flag | Run in interactive mode for single PDF processing |

### State Management

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--results-file` | `-r` | string | Path to results file (default: results/result.json) |
| `--download-only` | `-d` | flag | Only download results for previously processed slides |
| `--skip-processing` | | flag | Skip processing new slides, only download existing results |

### Cache Management

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--cache-list` | | flag | List all cached/processed files |
| `--cache-interactive` | | flag | Interactive cache management interface |
| `--cache-clean` | | flag | Clean all cached files (removes from results and output) |

### Utility

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--help` | `-h` | flag | Show help message and exit |

## Usage Patterns

### Course Processing

**Basic course scraping:**
```bash
python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"
```

**With keyword filtering:**
```bash
python main.py --url "https://example.com/course/" --keyword "lecture"
```

**Interactive course processing:**
```bash
python main.py --interactive
```

**Custom results file:**
```bash
python main.py --url "https://example.com/" --results-file "project1.json"
```

### Single PDF Processing

**Direct PDF processing:**
```bash
python main.py --pdf-url "https://example.com/document.pdf"
```

**With custom name:**
```bash
python main.py --pdf-url "https://example.com/doc.pdf" --pdf-name "Chapter 1 Introduction"
```

**Interactive PDF processing:**
```bash
python main.py --pdf-interactive
```

### State and Cache Management

**Download existing results:**
```bash
python main.py --download-only
```

**List cached files:**
```bash
python main.py --cache-list
```

**Interactive cache management:**
```bash
python main.py --cache-interactive
```

**Clean all cache:**
```bash
python main.py --cache-clean
```

**Cache management with custom results file:**
```bash
python main.py --cache-list --results-file "custom.json"
```

## Option Details

### --url (Course Processing)

Specifies the course schedule URL for scraping slides.

**Format**: Full HTTP/HTTPS URL
**Required**: When not using PDF mode or interactive mode
**Example**: `--url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"`

**Behavior**:
- Scrapes the webpage for PDF links
- Applies keyword filtering if specified
- Processes all found slides
- Skips already processed files

### --pdf-url (Single PDF Processing)

Process a single PDF file directly from URL.

**Format**: Full HTTP/HTTPS URL to PDF file
**Required**: When using single PDF mode
**Example**: `--pdf-url "https://example.com/lecture01.pdf"`

**Behavior**:
- Downloads and processes single PDF
- Auto-generates name from URL if --pdf-name not specified
- Creates task in same results tracking system

### --pdf-name (PDF Naming)

Custom name for PDF when using --pdf-url.

**Format**: String (automatically gets .pdf extension if missing)
**Optional**: Auto-generated from URL if not specified
**Example**: `--pdf-name "Introduction to Security"`

**Behavior**:
- Overrides auto-generated name from URL
- Used for tracking and output directory naming
- Automatically adds .pdf extension if missing

### --keyword (Filtering)

Filter slides by keyword in the link text or filename.

**Format**: String (case-insensitive matching)
**Optional**: No filtering if not specified
**Example**: `--keyword "lecture"`

**Behavior**:
- Matches against link text and URLs
- Case-insensitive search
- Excludes files containing "inked" (linked files)
- Applied before processing starts

### --interactive (Course Interactive Mode)

Launch interactive mode for course processing.

**Type**: Flag (no arguments)
**Behavior**:
- Prompts for course URL
- Prompts for optional keyword
- Same processing as command-line mode after input

**Interactive Flow**:
```
=== Slide Converter Setup ===
Enter the course schedule URL: [user input]
Enter keyword to filter slides (or press Enter to process all slides): [user input]
```

### --pdf-interactive (PDF Interactive Mode)

Launch interactive mode for single PDF processing.

**Type**: Flag (no arguments)
**Behavior**:
- Prompts for PDF URL
- Prompts for optional custom name
- Same processing as --pdf-url mode after input

**Interactive Flow**:
```
=== Single PDF Processing Setup ===
Enter the PDF URL: [user input]
Enter custom name for the PDF (or press Enter to auto-generate): [user input]
```

### --results-file (State File)

Specify custom results file for state tracking.

**Format**: File path (relative or absolute)
**Default**: `results/result.json`
**Example**: `--results-file "project1_results.json"`

**Behavior**:
- Creates file if it doesn't exist
- Loads previous state if file exists
- Used for all state operations (save, load, cache management)

### --download-only (Resume Downloads)

Skip processing and only download existing results.

**Type**: Flag (no arguments)
**Behavior**:
- Reads existing results file
- Downloads completed tasks that haven't been downloaded
- Skips all new processing
- Useful for resuming interrupted sessions

### --skip-processing (Download Mode)

Alternative flag for download-only behavior.

**Type**: Flag (no arguments)
**Behavior**: Identical to --download-only

### --cache-list (List Cache)

Display all cached/processed files with details.

**Type**: Flag (no arguments)
**Output Format**:
```
=== Cached Files ===
#    Name                                     State        Size       Created
--------------------------------------------------------------------------------
1    lecture01-intro.pdf                      done         2.5MB      2024-01-15 14:30
2    lecture02-crypto.pdf                     failed       N/A        2024-01-15 15:45
```

**Information Shown**:
- Reference number for interactive selection
- File name (truncated if long)
- Processing state
- Output directory size
- Creation timestamp

### --cache-interactive (Interactive Cache)

Launch interactive cache management interface.

**Type**: Flag (no arguments)
**Available Commands**:
- `<number>`: Delete specific file
- `<start>-<end>`: Delete range of files
- `all`: Delete all cached files
- `refresh`: Update the list
- `done`/`quit`: Exit

**Safety Features**:
- Confirmation prompts for all deletions
- Shows file count before bulk operations
- Real-time list updates

### --cache-clean (Clean All Cache)

Remove all cached files with confirmation.

**Type**: Flag (no arguments)
**Behavior**:
- Shows count of files to be deleted
- Requires explicit confirmation
- Removes from results file and deletes output directories
- Processes each file individually with status updates

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error or user cancellation |
| 2 | Invalid arguments or missing required options |

## Environment Variables

The tool respects these environment variables from `.env` file:

| Variable | Required | Description |
|----------|----------|-------------|
| `TOKEN` | Yes | MinerU API token for PDF processing |
| `GOOGLE_API_KEY` | No | Google API key for image captioning |

## Error Handling

### Graceful Recovery

The tool handles errors gracefully:
- **Network issues**: Automatic retries with backoff
- **Individual file failures**: Continues with remaining files
- **API errors**: Saves state and continues where possible
- **User interruption**: Saves current state on Ctrl+C

### State Preservation

State is automatically saved:
- After each successful task creation
- After each task completion or failure
- Before program exit (normal or error)
- During interactive operations

## Compatibility

### Python Version
- **Minimum**: Python 3.7
- **Recommended**: Python 3.8 or higher

### Operating Systems
- **Windows**: Full support
- **macOS**: Full support  
- **Linux**: Full support

### API Dependencies
- **MinerU API**: Required for PDF processing
- **Google Gemini API**: Optional for image captioning

## Examples by Use Case

### Academic Course Processing
```bash
# Process all slides from a course
python main.py --url "https://university.edu/course/schedule/"

# Process only lectures
python main.py --url "https://university.edu/course/schedule/" --keyword "lecture"

# Use interactive mode for easy input
python main.py --interactive
```

### Research Paper Processing
```bash
# Process individual papers
python main.py --pdf-url "https://arxiv.org/pdf/paper.pdf" --pdf-name "Research Paper Title"

# Interactive mode for papers
python main.py --pdf-interactive
```

### Batch Operations
```bash
# Process multiple courses with separate tracking
python main.py --url "https://course1.edu/" --results-file "course1.json"
python main.py --url "https://course2.edu/" --results-file "course2.json"

# Download all results
python main.py --download-only --results-file "course1.json"
python main.py --download-only --results-file "course2.json"
```

### Maintenance Operations
```bash
# Review what's been processed
python main.py --cache-list

# Clean up selectively
python main.py --cache-interactive

# Full cleanup
python main.py --cache-clean
```

For detailed usage examples and workflows, see the [Usage Guide](usage.md). 