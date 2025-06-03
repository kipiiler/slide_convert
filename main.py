import os
import json
import argparse
import sys
from urllib.parse import urlparse
from mineru_client import MinerUClient
from slide_scraper import SlideScraper
from zipper import download_and_extract_zip

def save_state(client: MinerUClient, results_file: str = 'results/result.json'):
    """Save current state to results file"""
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    tracked_requests = client.get_tracked_requests()
    with open(results_file, 'w') as f:
        json.dump(tracked_requests, f, indent=4)
    print(f"Results saved to {results_file}")

def process_slides(client: MinerUClient, slide_links: list):
    """Process slides and handle errors"""
    for slide in slide_links:
        try:
            # Create a task for each slide
            task_id = client.create_task(
                url=slide['url'],
                name=slide['name'],
                is_ocr=True,
                enable_formula=True,
                enable_table=True
            )
            print(f"Created task for {slide['name']} with ID: {task_id}")
            
            # Wait for the task to complete
            result = client.wait_for_task(slide['name'])
            print(f"Completed processing {slide['name']}")
            print(result)
            
        except Exception as e:
            print(f"Error processing {slide['name']}: {str(e)}")
            # Save state after error
            save_state(client)
            # Continue with next slide instead of stopping
            continue

def process_single_pdf(client: MinerUClient, pdf_url: str, pdf_name: str = None):
    """Process a single PDF URL"""
    try:
        # Generate name from URL if not provided
        if not pdf_name:
            parsed_url = urlparse(pdf_url)
            pdf_name = os.path.basename(parsed_url.path)
            if not pdf_name or not pdf_name.endswith('.pdf'):
                pdf_name = f"document_{int(time.time())}.pdf"
        
        # Ensure .pdf extension
        if not pdf_name.endswith('.pdf'):
            pdf_name += '.pdf'
        
        print(f"Processing single PDF: {pdf_name}")
        print(f"URL: {pdf_url}")
        
        # Create a task for the PDF
        task_id = client.create_task(
            url=pdf_url,
            name=pdf_name,
            is_ocr=True,
            enable_formula=True,
            enable_table=True
        )
        print(f"Created task for {pdf_name} with ID: {task_id}")
        
        # Wait for the task to complete
        result = client.wait_for_task(pdf_name)
        print(f"Completed processing {pdf_name}")
        print(result)
        
        return True
        
    except Exception as e:
        print(f"Error processing PDF {pdf_name}: {str(e)}")
        # Save state after error
        save_state(client)
        return False

def download_results(client: MinerUClient):
    """Download and extract results for completed tasks"""
    os.makedirs('output', exist_ok=True)
    tracked_requests = client.get_tracked_requests()
    
    for req in tracked_requests:
        try:
            if req['state'] == 'done' and req['result'] and 'full_zip_url' in req['result']:
                res = client.get_request_by_name(req['name'])
                download_url = res['result']['full_zip_url']
                download_and_extract_zip(download_url, req['name'])
                print(f"Downloaded and extracted results for {req['name']}")
            else:
                print(f"Skipping {req['name']} - not completed or no download URL")
        except Exception as e:
            print(f"Error downloading results for {req['name']}: {str(e)}")
            continue

def get_user_input():
    """Get course URL and keyword from user input"""
    print("=== Slide Converter Setup ===")
    
    # Get course URL
    course_url = input("Enter the course schedule URL: ").strip()
    if not course_url:
        print("Error: Course URL is required!")
        sys.exit(1)
    
    # Get keyword filter
    keyword = input("Enter keyword to filter slides (or press Enter to process all slides): ").strip()
    if not keyword:
        keyword = None
    
    return course_url, keyword

def get_pdf_input():
    """Get PDF URL and name from user input"""
    print("=== Single PDF Processing Setup ===")
    
    # Get PDF URL
    pdf_url = input("Enter the PDF URL: ").strip()
    if not pdf_url:
        print("Error: PDF URL is required!")
        sys.exit(1)
    
    # Get optional custom name
    pdf_name = input("Enter custom name for the PDF (or press Enter to auto-generate): ").strip()
    if not pdf_name:
        pdf_name = None
    
    return pdf_url, pdf_name

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Convert course slides to processed format using MinerU",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/" --keyword "slides"
  python main.py --pdf-url "https://example.com/lecture01.pdf"
  python main.py --pdf-url "https://example.com/lecture01.pdf" --pdf-name "Introduction to Security"
  python main.py --interactive
  python main.py --pdf-interactive
  python main.py --download-only
        """
    )
    
    parser.add_argument(
        '--url', '-u',
        type=str,
        help='Course schedule URL to scrape slides from'
    )
    
    parser.add_argument(
        '--pdf-url',
        type=str,
        help='Direct PDF URL to process (single file mode)'
    )
    
    parser.add_argument(
        '--pdf-name',
        type=str,
        help='Custom name for the PDF when using --pdf-url'
    )
    
    parser.add_argument(
        '--keyword', '-k',
        type=str,
        help='Keyword to filter slides (e.g., "slides", "lecture")'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode (prompts for course URL input)'
    )
    
    parser.add_argument(
        '--pdf-interactive',
        action='store_true',
        help='Run in interactive mode for single PDF processing'
    )
    
    parser.add_argument(
        '--results-file', '-r',
        type=str,
        default='results/result.json',
        help='Path to results file (default: results/result.json)'
    )
    
    parser.add_argument(
        '--download-only', '-d',
        action='store_true',
        help='Only download results for previously processed slides'
    )
    
    parser.add_argument(
        '--skip-processing',
        action='store_true',
        help='Skip processing new slides, only download existing results'
    )
    
    return parser.parse_args()

def main():
    try:
        import time  # Add missing import
        args = parse_arguments()
        
        # Initialize the MinerU client
        client = MinerUClient(results_file=args.results_file)
        
        # If download-only mode, skip to downloading
        if args.download_only or args.skip_processing:
            print("Skipping processing, downloading existing results...")
            download_results(client)
            return
        
        # Handle single PDF processing
        if args.pdf_interactive or args.pdf_url:
            if args.pdf_interactive:
                pdf_url, pdf_name = get_pdf_input()
            else:
                pdf_url = args.pdf_url
                pdf_name = args.pdf_name
            
            # Process single PDF
            success = process_single_pdf(client, pdf_url, pdf_name)
            
            # Print summary
            print("\nProcessing Summary:")
            tracked_requests = client.get_tracked_requests()
            completed = len([req for req in tracked_requests if req['state'] == 'done'])
            failed = len([req for req in tracked_requests if req['state'] == 'failed'])
            pending = len([req for req in tracked_requests if req['state'] in ['pending', 'running', 'converting']])
            
            print(f"Completed: {completed}")
            print(f"Failed: {failed}")
            print(f"Pending: {pending}")
            
            # Save final state
            save_state(client, args.results_file)
            
            # Download results
            print("\nDownloading results...")
            download_results(client)
            return
        
        # Handle course scraping mode
        # Determine how to get input
        if args.interactive or (not args.url and not args.download_only):
            course_url, keyword = get_user_input()
        else:
            course_url = args.url
            keyword = args.keyword
            
        if not course_url:
            print("Error: Course URL is required! Use --url, --interactive, --pdf-url, or --pdf-interactive")
            sys.exit(1)
        
        # Initialize the slide scraper
        print(f"Scraping slides from: {course_url}")
        scraper = SlideScraper(course_url)
        
        # Get all slide links
        slide_links = scraper.get_links(keyword)
        
        if not slide_links:
            print("No slides found matching the criteria!")
            return

        # Process slide names
        for slide in slide_links:
            if ".pdf" in slide['url'] and "/" in slide['url']:
                slide['name'] = slide['url'].split("/")[-1]

        # filter out slides that already exist and had been processed
        original_count = len(slide_links)
        slide_links = [slide for slide in slide_links 
                      if slide['name'] not in [req['name'] for req in client.get_tracked_requests() 
                                             if client.get_request_by_name(slide['name'])['state'] == 'done']]
        
        filtered_count = original_count - len(slide_links)
        if filtered_count > 0:
            print(f"Skipped {filtered_count} already processed slides")
        
        print(f"Processing {len(slide_links)} slides")
        
        if len(slide_links) == 0:
            print("All slides have already been processed!")
            print("Use --download-only to download existing results")
            return

        # Process slides
        process_slides(client, slide_links)
        
        # Print summary
        print("\nProcessing Summary:")
        tracked_requests = client.get_tracked_requests()
        completed = len([req for req in tracked_requests if req['state'] == 'done'])
        failed = len([req for req in tracked_requests if req['state'] == 'failed'])
        pending = len([req for req in tracked_requests if req['state'] in ['pending', 'running', 'converting']])
        
        print(f"Completed: {completed}")
        print(f"Failed: {failed}")
        print(f"Pending: {pending}")
        
        # Save final state
        save_state(client, args.results_file)
        
        # Download results
        print("\nDownloading results...")
        download_results(client)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        if 'client' in locals():
            save_state(client, args.results_file)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        # Save state even if fatal error occurs
        if 'client' in locals():
            save_state(client, args.results_file)
        raise

if __name__ == "__main__":
    main()
