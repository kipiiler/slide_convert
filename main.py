import os
import json
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

def main():
    try:
        # Initialize the slide scraper
        course_url = "https://courses.cs.washington.edu/courses/cse484/25sp/schedule/"
        scraper = SlideScraper(course_url)
        
        # Get all slide links
        slide_links = scraper.get_links("slides")
        
        # Initialize the MinerU client
        client = MinerUClient()

        # Process slide names
        for slide in slide_links:
            if ".pdf" in slide['url'] and "/" in slide['url']:
                slide['name'] = slide['url'].split("/")[-1]

        # filter out slides that already exist and had been processed
        for slide in slide_links:
            if slide['name'] in [req['name'] for req in client.get_tracked_requests()]:
                if client.get_request_by_name(slide['name'])['state'] == 'done':
                    slide_links.remove(slide)
        print(f"Processing {len(slide_links)} slides")

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
        save_state(client)
        
        # Download results
        print("\nDownloading results...")
        download_results(client)
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        # Save state even if fatal error occurs
        if 'client' in locals():
            save_state(client)
        raise

if __name__ == "__main__":
    main()
