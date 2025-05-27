from dotenv import load_dotenv
import requests
import os
import time
import json
from typing import Dict, Optional, List
from enum import Enum

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    CONVERTING = "converting"
    COMPLETED = "done"
    FAILED = "failed"

class MinerUClient:
    def __init__(self, results_file: str = 'results/result.json'):
        load_dotenv()
        self.token = os.getenv('TOKEN')
        if not self.token:
            raise ValueError("TOKEN environment variable not found")
        
        self.base_url = 'https://mineru.net/api/v4/extract'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        self.requests_tracker: Dict[str, Dict] = {}
        self.results_file = results_file
        
        # Try to load previous state if results file exists
        self.load_previous_state()

    def load_previous_state(self) -> None:
        """Load previous task states from results file if it exists"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    previous_requests = json.load(f)
                
                # Convert the list of requests back to the tracker dictionary
                for req in previous_requests:
                    name = req['name']
                    self.requests_tracker[name] = {
                        'task_id': req['task_id'],
                        'url': req['url'],
                        'state': req['state'],
                        'created_at': req['created_at'],
                        'progress': req['progress'],
                        'error_message': req['error_message'],
                        'result': req['result']
                    }
                print(f"Loaded {len(previous_requests)} previous tasks from {self.results_file}")
            except Exception as e:
                print(f"Error loading previous state: {str(e)}")

    def save_current_state(self) -> None:
        """Save current task states to results file"""
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump(self.get_tracked_requests(), f, indent=4)
        print(f"Saved current state to {self.results_file}")

    def get_completed_tasks(self) -> List[Dict]:
        """Get all tasks that have been completed successfully"""
        return [
            req for req in self.get_tracked_requests()
            if req['state'] == TaskState.COMPLETED.value
        ]

    def get_failed_tasks(self) -> List[Dict]:
        """Get all tasks that have failed"""
        return [
            req for req in self.get_tracked_requests()
            if req['state'] == TaskState.FAILED.value
        ]

    def get_pending_tasks(self) -> List[Dict]:
        """Get all tasks that are still pending or running"""
        return [
            req for req in self.get_tracked_requests()
            if req['state'] in [TaskState.PENDING.value, TaskState.RUNNING.value, TaskState.CONVERTING.value]
        ]

    def create_task(self, url: str, name: str, is_ocr: bool = True, 
                   enable_formula: bool = True, enable_table: bool = True, 
                   language: str = 'en') -> str:
        """
        Create a new extraction task
        
        Args:
            url: URL of the PDF to process
            name: Custom name for tracking this request
            is_ocr: Whether to perform OCR
            enable_formula: Whether to extract formulas
            enable_table: Whether to extract tables
            language: Language of the document
            
        Returns:
            task_id: The ID of the created task
        """
        # Check if task already exists
        if name in self.requests_tracker:
            print(f"Task {name} already exists with state: {self.get_state_description(self.requests_tracker[name]['state'])}")
            return self.requests_tracker[name]['task_id']

        endpoint = f"{self.base_url}/task"
        data = {
            'url': url,
            'is_ocr': is_ocr,
            'enable_formula': enable_formula,
            'enable_table': enable_table,
            'language': language,
        }
        
        print(data)
        response = requests.post(endpoint, headers=self.headers, json=data)
        print(response.status_code)
        print(response.json())
        print(response.json()["data"])
        
        task_id = response.json()["data"]["task_id"]
        
        # Track the request
        self.requests_tracker[name] = {
            'task_id': task_id,
            'url': url,
            'state': TaskState.PENDING.value,
            'created_at': time.time(),
            'result': None,
            'progress': None,
            'error_message': None
        }
        
        # Save state after creating new task
        self.save_current_state()
        
        return task_id

    def get_task_status(self, task_id: str) -> Dict:
        """
        Get the status of a task
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            Dict containing task status and data
        """
        endpoint = f"{self.base_url}/task/{task_id}"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]

    def get_state_description(self, state: str) -> str:
        """Get a human-readable description of the task state"""
        state_descriptions = {
            TaskState.PENDING.value: "Task is in queue",
            TaskState.RUNNING.value: "Task is being processed",
            TaskState.CONVERTING.value: "Task is being converted",
            TaskState.COMPLETED.value: "Task completed successfully",
            TaskState.FAILED.value: "Task failed"
        }
        return state_descriptions.get(state, f"Unknown state: {state}")

    def wait_for_task(self, name: str, timeout: int = 300, check_interval: int = 5) -> Dict:
        """
        Wait for a task to complete
        
        Args:
            name: Name of the tracked request
            timeout: Maximum time to wait in seconds
            check_interval: Time between status checks in seconds
            
        Returns:
            Dict containing the final task result
        """
        if name not in self.requests_tracker:
            raise ValueError(f"No tracked request found with name: {name}")
            
        # If task is already completed, return the result
        if self.requests_tracker[name]['state'] == TaskState.COMPLETED.value:
            print(f"Task {name} was already completed")
            return self.requests_tracker[name]['result']
            
        # If task failed, raise the error
        if self.requests_tracker[name]['state'] == TaskState.FAILED.value:
            error_msg = self.requests_tracker[name]['error_message']
            raise Exception(f"Task failed: {error_msg}")
            
        task_id = self.requests_tracker[name]['task_id']
        start_time = time.time()
        last_state = None

        print(f"Waiting for task {name} to complete...")
        
        while time.time() - start_time < timeout:
            status_data = self.get_task_status(task_id)
            current_state = status_data['state']
            
            # Only print state changes
            if current_state != last_state:
                print(f"Task state: {self.get_state_description(current_state)}")
                last_state = current_state
            
            self.requests_tracker[name]['state'] = current_state
            
            # Update progress if available
            if 'extract_progress' in status_data:
                self.requests_tracker[name]['progress'] = status_data['extract_progress']
                progress = status_data['extract_progress']
                print(f"Progress: {progress['extracted_pages']}/{progress['total_pages']} pages")
            
            if current_state == TaskState.COMPLETED.value:
                self.requests_tracker[name]['result'] = status_data
                # Save state after task completion
                self.save_current_state()
                return status_data
            elif current_state == TaskState.FAILED.value:
                error_msg = status_data.get('err_msg', 'Unknown error')
                self.requests_tracker[name]['error_message'] = error_msg
                self.requests_tracker[name]['result'] = status_data
                # Save state after task failure
                self.save_current_state()
                raise Exception(f"Task failed: {error_msg}")
                
            time.sleep(check_interval)
            
        raise TimeoutError(f"Task did not complete within {timeout} seconds")

    def get_tracked_requests(self) -> List[Dict]:
        """
        Get information about all tracked requests
        
        Returns:
            List of dictionaries containing request information
        """
        return [
            {
                'name': name,
                'task_id': info['task_id'],
                'url': info['url'],
                'state': info['state'],
                'state_description': self.get_state_description(info['state']),
                'created_at': info['created_at'],
                'progress': info['progress'],
                'error_message': info['error_message'],
                'result': info['result']
            }
            for name, info in self.requests_tracker.items()
        ]

    def get_request_by_name(self, name: str) -> Optional[Dict]:
        """
        Get information about a specific tracked request
        
        Args:
            name: Name of the tracked request
            
        Returns:
            Dict containing request information or None if not found
        """
        if name in self.requests_tracker:
            info = self.requests_tracker[name]
            return {
                'name': name,
                'state_description': self.get_state_description(info['state']),
                **info
            }
        return None

# Example usage
if __name__ == "__main__":
    client = MinerUClient()
    
    # Create a task
    task_id = client.create_task(
        url="https://courses.cs.washington.edu/courses/cse484/25sp/slides/cse484-lecture1-25sp.pdf",
        name="lecture1_slides"
    )
    
    # Wait for completion
    try:
        result = client.wait_for_task("lecture1_slides")
        print("Task completed successfully!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get all tracked requests
    tracked_requests = client.get_tracked_requests()
    print("\nTracked Requests:")
    for req in tracked_requests:
        print(f"- {req['name']}: {req['state']}") 