# Cache Management Guide

The Slide Converter includes comprehensive cache management features to help you view, organize, and clean up processed files efficiently.

## Overview

The cache management system tracks:
- **Processing State**: Current status of each file (pending, running, done, failed)
- **File Metadata**: Creation time, file names, original URLs
- **Output Directories**: Automatically linked processed content
- **Storage Usage**: Size information for each processed file

## Cache Commands

### List Cached Files

View all processed files with detailed information:

```bash
python main.py --cache-list
```

**Output Example:**
```
=== Cached Files ===
#    Name                                     State        Size       Created
--------------------------------------------------------------------------------
1    lecture01-intro.pdf                      done         2.5MB      2024-01-15 14:30
2    lecture02-crypto.pdf                     done         1.8MB      2024-01-15 15:45
3    lecture03-auth.pdf                       failed       N/A        2024-01-15 16:20
4    assignment01.pdf                         pending      N/A        2024-01-15 17:00
```

**Information Displayed:**
- **#**: Reference number for easy selection
- **Name**: File name (truncated if longer than 39 characters)
- **State**: Current processing status
- **Size**: Output directory size in human-readable format
- **Created**: When the processing task was created

### Interactive Cache Management

Launch the interactive interface for selective file management:

```bash
python main.py --cache-interactive
```

This opens a command-driven interface where you can selectively delete files.

## Interactive Commands

### Single File Deletion

Delete a specific file by its number:

```
Enter your choice: 3
Delete 'lecture03-auth.pdf'? (yes/no): yes
```

This will:
1. Remove the entry from `results.json`
2. Delete the corresponding output directory
3. Show confirmation of actions taken

### Range Deletion

Delete multiple files at once using range syntax:

```
Enter your choice: 1-3
Delete 3 files (1-3)? (yes/no): yes
```

**Range Examples:**
- `1-5`: Delete files 1 through 5
- `2-4`: Delete files 2, 3, and 4
- `1-1`: Delete only file 1 (same as single deletion)

### Bulk Operations

Delete all cached files:

```
Enter your choice: all
Are you sure you want to delete ALL 4 cached files? (yes/no): yes
```

### Utility Commands

**Refresh the list:**
```
Enter your choice: refresh
```
Updates the display with current cache state.

**Exit cache management:**
```
Enter your choice: done
# or
Enter your choice: quit
```

## Clean All Cache

Remove all cached files with a single command:

```bash
python main.py --cache-clean
```

**Safety Features:**
- Confirmation prompt before any deletion
- Shows count of files to be deleted
- Processes each file individually with status updates

**Example Session:**
```
Are you sure you want to clean ALL cached files? This will delete results and output directories. (yes/no): yes
Found 4 cached files
Removed 'lecture01-intro.pdf' from results cache
Deleted output directory: output/lecture01-intro.pdf
Removed 'lecture02-crypto.pdf' from results cache
Deleted output directory: output/lecture02-crypto.pdf
...
All cache cleaned.
```

## File States

Understanding processing states helps manage your cache effectively:

### State Descriptions

- **pending**: Task created, waiting to start processing
- **running**: Currently being processed by MinerU
- **converting**: Converting to final format
- **done**: Successfully completed, results available
- **failed**: Processing failed with error

### State-Based Management

**Clean up failed files:**
```bash
# Use interactive mode to see failed files
python main.py --cache-interactive
# Then delete only failed entries (they show as "failed" state)
```

**Keep completed files, remove pending:**
```bash
# Use cache list to identify pending/failed files
python main.py --cache-list
# Use interactive mode to selectively remove
python main.py --cache-interactive
```

## Storage Management

### Understanding Size Information

File sizes shown represent the total size of extracted content:
- **Markdown files**: Converted text content
- **Images**: Extracted figures and diagrams
- **Metadata**: Processing information and logs

**Size Formats:**
- `B`: Bytes
- `KB`: Kilobytes
- `MB`: Megabytes
- `GB`: Gigabytes

### Storage Optimization

**Find large files:**
```bash
python main.py --cache-list
# Look at the Size column to identify large outputs
```

**Clean up space efficiently:**
1. Use `--cache-list` to identify largest files
2. Use `--cache-interactive` to selectively remove large or unwanted files
3. Keep frequently accessed or important results

## Advanced Cache Operations

### Working with Multiple Result Files

If you use different result files for different projects:

```bash
# List cache for specific project
python main.py --cache-list --results-file "project1.json"

# Clean specific project cache
python main.py --cache-clean --results-file "project1.json"

# Interactive management for specific project
python main.py --cache-interactive --results-file "project1.json"
```

### Selective Cleanup Strategies

**Development workflow:**
```bash
# During development, clean failed/pending regularly
python main.py --cache-interactive
# Select and remove failed entries

# Keep successful results for reference
python main.py --cache-list
# Review completed files
```

**Production workflow:**
```bash
# Process files
python main.py --url "https://example.com"

# Archive important results
# (manually copy important output directories)

# Clean cache for next batch
python main.py --cache-clean
```

## Best Practices

### Regular Maintenance

1. **Review cache weekly**: Use `--cache-list` to see accumulated files
2. **Clean failed entries**: Remove failed processing attempts that won't be retried
3. **Archive important results**: Copy critical outputs before cleaning
4. **Monitor storage**: Keep track of output directory sizes

### Selective Retention

Keep files that are:
- **Successfully processed** and frequently referenced
- **Large or time-consuming** to reprocess
- **Part of ongoing projects**

Remove files that are:
- **Failed processing** attempts
- **Test runs** or experimental processing
- **Easily reproducible** from original sources
- **No longer needed** for current projects

### Safety Guidelines

1. **Always confirm deletions**: The tool requires explicit confirmation
2. **Check before bulk operations**: Review the list before using `all` command
3. **Backup important results**: Copy critical outputs before cleaning
4. **Use range deletion carefully**: Double-check range syntax (1-3, not 1,3)

## Troubleshooting

### Common Issues

**"Output directory not found"**
- Normal when results haven't been downloaded yet
- Use `--download-only` to download missing results

**Permission errors during deletion**
- Close any programs accessing the output directories
- Run with administrator privileges if needed

**Cache shows files but directories missing**
- Results metadata exists but outputs weren't downloaded
- Use `--download-only` to restore missing outputs

### Recovery Operations

**Restore missing outputs:**
```bash
python main.py --download-only
```

**Fix inconsistent cache state:**
```bash
# List current cache
python main.py --cache-list

# Clean problematic entries
python main.py --cache-interactive
# Remove entries with missing outputs

# Reprocess if needed
python main.py --url "original-source-url"
```

## Integration with Other Features

Cache management works seamlessly with other tool features:

- **Processing**: New files automatically added to cache
- **Downloads**: `--download-only` respects cache state
- **AI Captioning**: Works with cached output directories
- **Resume Operations**: Cache enables resuming from interruptions

See the [Usage Guide](usage.md) for information on integrating cache management with your workflow. 