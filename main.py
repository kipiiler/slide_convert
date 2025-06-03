import argparse
import os
import sys
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from slide_scraper import SlideScraper
from mineru_client import MinerUClient, TaskState
from zipper import download_and_extract_zip


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Extract and process slides from course websites or local files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Course scraping
  python main.py --interactive
  python main.py --url "https://example.com/schedule/" --keyword "lecture"
  
  # Single PDF processing
  python main.py --pdf-url "https://example.com/file.pdf"
  python main.py --pdf-interactive
  
  # Local file processing
  python main.py --local-file "document.pdf"
  python main.py --local-interactive
  
  # Cache management
  python main.py --cache-list
  python main.py --cache-interactive
        """
    )
    
    # Course processing options
    course_group = parser.add_argument_group('Course Processing')
    course_group.add_argument('--url', '-u', type=str, help='Course schedule URL to scrape slides from')
    course_group.add_argument('--keyword', '-k', type=str, help='Keyword to filter slides (e.g., "slides", "lecture")')
    course_group.add_argument('--interactive', '-i', action='store_true', 
                             help='Run in interactive mode (prompts for course URL input)')
    
    # Single PDF processing options
    pdf_group = parser.add_argument_group('Single PDF Processing')
    pdf_group.add_argument('--pdf-url', type=str, help='Direct PDF URL to process (single file mode)')
    pdf_group.add_argument('--pdf-name', type=str, help='Custom name for the PDF when using --pdf-url')
    pdf_group.add_argument('--pdf-interactive', action='store_true',
                          help='Run in interactive mode for single PDF processing')
    
    # Local file processing options
    local_group = parser.add_argument_group('Local File Processing')
    local_group.add_argument('--local-file', type=str, help='Path to local PDF file to process')
    local_group.add_argument('--local-name', type=str, help='Custom name for the local file')
    local_group.add_argument('--local-interactive', action='store_true',
                            help='Run in interactive mode for local file processing')
    
    # State management options
    state_group = parser.add_argument_group('State Management')
    state_group.add_argument('--results-file', '-r', type=str, default='results/result.json',
                            help='Path to results file (default: results/result.json)')
    state_group.add_argument('--download-only', '-d', action='store_true',
                            help='Only download results for previously processed slides')
    state_group.add_argument('--skip-processing', action='store_true',
                            help='Skip processing new slides, only download existing results')
    
    # Cache management options
    cache_group = parser.add_argument_group('Cache Management')
    cache_group.add_argument('--cache-list', action='store_true',
                            help='List all cached/processed files')
    cache_group.add_argument('--cache-interactive', action='store_true',
                            help='Interactive cache management interface')
    cache_group.add_argument('--cache-clean', action='store_true',
                            help='Clean all cached files (removes from results and output)')
    
    return parser


def validate_arguments(args) -> None:
    """Validate command line arguments for conflicts and requirements"""
    # Count the number of main modes selected
    main_modes = [
        args.url or args.interactive,
        args.pdf_url or args.pdf_interactive,
        args.local_file or args.local_interactive,
        args.download_only or args.skip_processing,
        args.cache_list or args.cache_interactive or args.cache_clean
    ]
    
    selected_modes = sum(1 for mode in main_modes if mode)
    
    if selected_modes == 0:
        print("Error: No operation specified. Use --help for usage information.")
        sys.exit(2)
    
    if selected_modes > 1:
        print("Error: Multiple operations specified. Please choose only one operation at a time.")
        sys.exit(2)
    
    # Validate specific argument combinations
    if args.pdf_name and not args.pdf_url:
        print("Error: --pdf-name can only be used with --pdf-url")
        sys.exit(2)
    
    if args.local_name and not args.local_file:
        print("Error: --local-name can only be used with --local-file")
        sys.exit(2)
    
    if args.keyword and not (args.url or args.interactive):
        print("Error: --keyword can only be used with course scraping (--url or --interactive)")
        sys.exit(2)
    
    # Validate local file exists
    if args.local_file and not os.path.exists(args.local_file):
        print(f"Error: Local file not found: {args.local_file}")
        sys.exit(2)


def get_course_input() -> tuple[str, Optional[str]]:
    """Get course URL and keyword from user input"""
    print("\n=== Slide Converter Setup ===")
    
    url = input("Enter the course schedule URL: ").strip()
    if not url:
        print("Error: URL cannot be empty")
        sys.exit(1)
    
    keyword = input("Enter keyword to filter slides (or press Enter to process all slides): ").strip()
    keyword = keyword if keyword else None
    
    return url, keyword


def get_pdf_input() -> tuple[str, Optional[str]]:
    """Get PDF URL and optional name from user input"""
    print("\n=== Single PDF Processing Setup ===")
    
    pdf_url = input("Enter the PDF URL: ").strip()
    if not pdf_url:
        print("Error: PDF URL cannot be empty")
        sys.exit(1)
    
    pdf_name = input("Enter custom name for the PDF (or press Enter to auto-generate): ").strip()
    pdf_name = pdf_name if pdf_name else None
    
    return pdf_url, pdf_name


def get_local_file_input() -> tuple[str, Optional[str]]:
    """Get local file path and optional name from user input"""
    print("\n=== Local File Processing Setup ===")
    
    file_path = input("Enter the path to the local PDF file: ").strip()
    if not file_path:
        print("Error: File path cannot be empty")
        sys.exit(1)
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    local_name = input("Enter custom name for the file (or press Enter to auto-generate): ").strip()
    local_name = local_name if local_name else None
    
    return file_path, local_name


def extract_filename_from_url(url: str) -> str:
    """Extract filename from URL, handling various URL formats"""
    # Remove query parameters and fragments
    clean_url = url.split('?')[0].split('#')[0]
    # Get the last part of the path
    filename = clean_url.split('/')[-1]
    
    # If no extension or not a PDF, generate a name with timestamp
    if not filename or not filename.lower().endswith('.pdf'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"document_{timestamp}.pdf"
    
    return filename


def process_single_pdf(client: MinerUClient, pdf_url: str, pdf_name: Optional[str] = None) -> None:
    """Process a single PDF from URL"""
    if not pdf_name:
        pdf_name = extract_filename_from_url(pdf_url)
    
    # Ensure .pdf extension
    if not pdf_name.lower().endswith('.pdf'):
        pdf_name += '.pdf'
    
    print(f"\nProcessing single PDF: {pdf_name}")
    print(f"URL: {pdf_url}")
    
    try:
        task_id = client.create_task(
            url=pdf_url,
            name=pdf_name,
            is_ocr=True,
            enable_formula=True,
            enable_table=True,
            language='en'
        )
        
        print(f"Created task with ID: {task_id}")
        print("Waiting for processing to complete...")
        
        result = client.wait_for_task(pdf_name, timeout=600)
        print(f"Processing completed successfully!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")


def process_local_file(client: MinerUClient, file_path: str, local_name: Optional[str] = None) -> None:
    """Process a local PDF file"""
    if not local_name:
        local_name = os.path.basename(file_path)
    
    # Ensure .pdf extension
    if not local_name.lower().endswith('.pdf'):
        local_name += '.pdf'
    
    print(f"\nProcessing local file: {local_name}")
    print(f"File path: {file_path}")
    
    try:
        batch_id = client.create_local_file_task(
            file_path=file_path,
            name=local_name,
            is_ocr=True,
            enable_formula=True,
            enable_table=True,
            language='en'
        )
        
        print(f"Created batch with ID: {batch_id}")
        print("Waiting for processing to complete...")
        
        result = client.wait_for_task(local_name, timeout=600)
        print(f"Processing completed successfully!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error processing local file: {str(e)}")


def download_results(client: MinerUClient) -> None:
    """Download results for completed tasks"""
    completed_tasks = client.get_completed_tasks()
    
    if not completed_tasks:
        print("No completed tasks found to download.")
        return
    
    print(f"Found {len(completed_tasks)} completed tasks to download.")
    
    for task in completed_tasks:
        try:
            if task['result'] and 'full_zip_url' in task['result']:
                zip_url = task['result']['full_zip_url']
                # Pass just the task name - zipper.py will create output/{task_name} automatically
                task_name = task['name']
                
                print(f"Downloading results for: {task_name}")
                download_and_extract_zip(zip_url, task_name)
                print(f"Results saved to: output/{task_name}")
            else:
                print(f"No download URL available for: {task['name']}")
                
        except Exception as e:
            print(f"Error downloading {task['name']}: {str(e)}")


def get_directory_size(path: str) -> int:
    """Calculate total size of directory in bytes"""
    total_size = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    return total_size


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format"""
    if size_bytes == 0:
        return "N/A"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable format"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')


def list_cached_files(client: MinerUClient) -> List[Dict]:
    """List all cached files with their information"""
    cached_files = client.get_tracked_requests()
    
    if not cached_files:
        print("No cached files found.")
        return []
    
    print("\n=== Cached Files ===")
    print(f"{'#':<4} {'Name':<40} {'State':<12} {'Size':<10} {'Created'}")
    print("-" * 80)
    
    for i, file_info in enumerate(cached_files, 1):
        name = file_info['name']
        if len(name) > 39:
            name = name[:36] + "..."
        
        state = file_info['state']
        created = format_timestamp(file_info['created_at'])
        
        # Calculate output directory size
        output_dir = f"output/{file_info['name']}"
        size = get_directory_size(output_dir)
        size_str = format_size(size)
        
        print(f"{i:<4} {name:<40} {state:<12} {size_str:<10} {created}")
    
    return cached_files


def delete_cached_file(client: MinerUClient, file_info: Dict) -> bool:
    """Delete a cached file and its output directory"""
    name = file_info['name']
    
    try:
        # Remove from results tracker
        if name in client.requests_tracker:
            del client.requests_tracker[name]
            print(f"Removed '{name}' from results cache")
        
        # Delete output directory
        output_dir = f"output/{name}"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"Deleted output directory: {output_dir}")
        
        # Save updated state
        client.save_current_state()
        return True
        
    except Exception as e:
        print(f"Error deleting {name}: {str(e)}")
        return False


def parse_range(range_str: str, max_num: int) -> List[int]:
    """Parse range string like '1-3' into list of numbers"""
    try:
        if '-' in range_str:
            start, end = range_str.split('-', 1)
            start_num = int(start.strip())
            end_num = int(end.strip())
            
            if start_num < 1 or end_num > max_num or start_num > end_num:
                raise ValueError("Invalid range")
            
            return list(range(start_num, end_num + 1))
        else:
            num = int(range_str.strip())
            if num < 1 or num > max_num:
                raise ValueError("Invalid number")
            return [num]
    except ValueError:
        raise ValueError(f"Invalid range format: {range_str}")


def interactive_cache_management(client: MinerUClient) -> None:
    """Interactive cache management interface"""
    while True:
        cached_files = list_cached_files(client)
        
        if not cached_files:
            print("No cached files to manage.")
            break
        
        print(f"\nEnter choice:")
        print("  - Number (e.g. '3'): Delete specific file")
        print("  - Range (e.g. '1-3'): Delete multiple files")
        print("  - 'all': Delete all cached files")
        print("  - 'refresh': Refresh the list")
        print("  - 'done' or 'quit': Exit")
        
        choice = input("Enter your choice: ").strip().lower()
        
        if choice in ['done', 'quit', 'exit']:
            print("Cache management completed.")
            break
        elif choice == 'refresh':
            continue
        elif choice == 'all':
            confirm = input(f"Are you sure you want to delete ALL {len(cached_files)} cached files? (yes/no): ").strip().lower()
            if confirm == 'yes':
                deleted_count = 0
                for file_info in cached_files:
                    if delete_cached_file(client, file_info):
                        deleted_count += 1
                print(f"Deleted {deleted_count} cached files.")
            else:
                print("Operation cancelled.")
        else:
            try:
                if '-' in choice or choice.isdigit():
                    indices = parse_range(choice, len(cached_files))
                    files_to_delete = [cached_files[i-1] for i in indices]
                    
                    if len(files_to_delete) == 1:
                        file_name = files_to_delete[0]['name']
                        confirm = input(f"Delete '{file_name}'? (yes/no): ").strip().lower()
                    else:
                        file_names = [f['name'] for f in files_to_delete]
                        print(f"Files to delete: {', '.join(file_names)}")
                        confirm = input(f"Delete {len(files_to_delete)} files ({choice})? (yes/no): ").strip().lower()
                    
                    if confirm == 'yes':
                        deleted_count = 0
                        for file_info in files_to_delete:
                            if delete_cached_file(client, file_info):
                                deleted_count += 1
                        print(f"Deleted {deleted_count} files.")
                    else:
                        print("Operation cancelled.")
                else:
                    print(f"Invalid choice: {choice}")
                    
            except ValueError as e:
                print(f"Error: {str(e)}")
            except (IndexError, KeyError):
                print("Invalid selection number.")


def clean_all_cache(client: MinerUClient) -> None:
    """Clean all cached files with confirmation"""
    cached_files = client.get_tracked_requests()
    
    if not cached_files:
        print("No cached files found to clean.")
        return
    
    print(f"Found {len(cached_files)} cached files")
    confirm = input("Are you sure you want to clean ALL cached files? This will delete results and output directories. (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    deleted_count = 0
    for file_info in cached_files:
        if delete_cached_file(client, file_info):
            deleted_count += 1
    
    print(f"All cache cleaned. Removed {deleted_count} files.")


def process_course_slides(client: MinerUClient, url: str, keyword: Optional[str] = None) -> None:
    """Process slides from a course website"""
    print(f"\nScraping slides from: {url}")
    if keyword:
        print(f"Filtering by keyword: {keyword}")
    
    # Initialize the slide scraper
    scraper = SlideScraper()
    
    # Scrape for slides
    slides = scraper.get_slides(url, keyword)
    
    if not slides:
        print("No slides found.")
        return
    
    print(f"Found {len(slides)} slides to process.")
    
    # Check which slides are already processed
    existing_requests = client.get_tracked_requests()
    existing_names = {req['name'] for req in existing_requests}
    
    new_slides = []
    for slide in slides:
        if slide['name'] not in existing_names:
            new_slides.append(slide)
        else:
            print(f"Skipping already processed: {slide['name']}")
    
    if not new_slides:
        print("All slides have already been processed.")
        download_results(client)
        return
    
    print(f"Processing {len(new_slides)} new slides...")
    
    # Create tasks for each new slide
    for i, slide in enumerate(new_slides, 1):
        print(f"\n[{i}/{len(new_slides)}] Creating task for: {slide['name']}")
        try:
            task_id = client.create_task(
                url=slide['url'],
                name=slide['name'],
                is_ocr=True,
                enable_formula=True,
                enable_table=True,
                language='en'
            )
            print(f"Created task with ID: {task_id}")
        except Exception as e:
            print(f"Error creating task for {slide['name']}: {str(e)}")
    
    # Wait for all tasks to complete
    print(f"\nWaiting for all tasks to complete...")
    for i, slide in enumerate(new_slides, 1):
        print(f"\n[{i}/{len(new_slides)}] Waiting for: {slide['name']}")
        try:
            result = client.wait_for_task(slide['name'], timeout=600)
            print(f"✓ Completed: {slide['name']}")
        except Exception as e:
            print(f"✗ Failed: {slide['name']} - {str(e)}")
    
    # Download all results
    print(f"\nDownloading results...")
    download_results(client)
    
    print(f"\nProcessing complete!")


def main():
    """Main function"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    validate_arguments(args)
    
    try:
        # Initialize the MinerU client
        client = MinerUClient(results_file=args.results_file)
        
        # Handle different modes of operation
        if args.cache_list:
            list_cached_files(client)
            
        elif args.cache_interactive:
            interactive_cache_management(client)
            
        elif args.cache_clean:
            clean_all_cache(client)
            
        elif args.download_only or args.skip_processing:
            download_results(client)
            
        elif args.interactive:
            url, keyword = get_course_input()
            process_course_slides(client, url, keyword)
            
        elif args.pdf_interactive:
            pdf_url, pdf_name = get_pdf_input()
            process_single_pdf(client, pdf_url, pdf_name)
            
        elif args.local_interactive:
            file_path, local_name = get_local_file_input()
            process_local_file(client, file_path, local_name)
            
        elif args.url:
            process_course_slides(client, args.url, args.keyword)
            
        elif args.pdf_url:
            process_single_pdf(client, args.pdf_url, args.pdf_name)
            
        elif args.local_file:
            process_local_file(client, args.local_file, args.local_name)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        # Save current state before exiting
        try:
            client.save_current_state()
            print("Current progress has been saved.")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
