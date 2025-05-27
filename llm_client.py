from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def setup(self) -> None:
        """Setup the LLM client with necessary configurations"""
        pass
    
    @abstractmethod
    def analyze_image(self, image_path: str, prompt: str) -> Optional[str]:
        """Analyze an image and return the response"""
        pass

class GeminiClient(LLMClient):
    """Google Gemini implementation of LLM client"""
    
    def __init__(self, model_name: str = 'gemini-2.0-flash-lite', rate_limit: int = 30):
        self.model_name = model_name
        self.model = None
        self.rate_limit = rate_limit  # Requests per minute
        self.request_count = 0
        self.start_time = None
        self.setup()
    
    def setup(self) -> None:
        """Setup Gemini API with API key"""
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        current_time = time.time()
        
        # Initialize start time if this is the first request
        if self.start_time is None:
            self.start_time = current_time
            self.request_count = 1
            return
        
        # If we've hit the rate limit and it's been less than a minute
        if self.request_count >= self.rate_limit:
            elapsed_time = current_time - self.start_time
            if elapsed_time < 60:  # Less than 1 minute
                # Wait for the remaining time
                wait_time = 60 - elapsed_time
                print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                # Reset counters
                self.start_time = time.time()
                self.request_count = 1
            else:
                # Reset counters if more than a minute has passed
                self.start_time = current_time
                self.request_count = 1
        else:
            # Increment request count
            self.request_count += 1
    
    def analyze_image(self, image_path: str, prompt: str) -> Optional[str]:
        """Analyze image using Gemini with rate limiting"""
        try:
            # Check rate limit before making request
            self._check_rate_limit()
            
            # Load and prepare the image
            image = Image.open(image_path)
            
            # Generate response
            response = self.model.generate_content(
                [prompt, image],
            )
            
            return response.text
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return None

class ImageCaptionAgent:
    """Agent for generating image captions in markdown files"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.image_prompt = """
        Analyze this image from a computer security lecture slide. Write a short and concise caption for the image that is use for accessibility (alt text for image).

        Give back only the caption, no other text, no markdown formatting, no code block, no code, no nothing.
        """
    
    def process_directory(self, directory_path: str) -> None:
        """Process all images in a directory and update markdown"""
        # Read the original markdown
        md_path = os.path.join(directory_path, 'full.md')
        if not os.path.exists(md_path):
            raise FileNotFoundError(f"Markdown file not found: {md_path}")
        
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image references
        import re
        image_pattern = r'!\[(.*?)\]\((.*?)\)'
        image_matches = re.finditer(image_pattern, content)
        
        # Process each image
        for match in image_matches:
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Skip if image already has alt text
            if alt_text and alt_text.strip():
                continue
            
            # Get full image path
            full_image_path = os.path.join(directory_path, image_path)
            if not os.path.exists(full_image_path):
                print(f"Warning: Image not found: {full_image_path}")
                continue
            
            # Generate caption
            print(f"Processing image: {image_path}")
            caption = self.llm_client.analyze_image(full_image_path, self.image_prompt)
            
            if caption:
                # Update the markdown content
                new_alt_text = caption.strip()
                content = content.replace(match.group(0), f'![{new_alt_text}]({image_path})')
                print(f"Generated caption: {new_alt_text}")
            else:
                print(f"Failed to generate caption for: {image_path}")
        
        # Write the updated content
        output_path = os.path.join(directory_path, 'captioned.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\nUpdated markdown saved to: {output_path}")

def main():
    # Example usage
    llm_client = GeminiClient()
    agent = ImageCaptionAgent(llm_client)

    dirs = "output/"
    for dir in os.listdir(dirs):
        directory_path = os.path.join(dirs, dir)
        agent.process_directory(directory_path)
    
    # Process a directory
    # directory_path = "C:/Users/nguye/Desktop/slide_convert/output/cse484-lecture16-25sp.pdf"
    # agent.process_directory(directory_path)

if __name__ == "__main__":
    main() 