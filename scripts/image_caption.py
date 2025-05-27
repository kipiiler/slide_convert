import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

def setup_gemini():
    """Setup Gemini API with API key"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    genai.configure(api_key=api_key)
    # Use Gemini 2.0 Flash Lite model
    return genai.GenerativeModel('gemini-2.0-flash-lite')

def analyze_image(model, image_path: str, prompt: str = "Describe this image in detail (short and concise). Focus on any text, diagrams, or technical content."):
    """Analyze image using Gemini"""
    try:
        # Load and prepare the image
        image = Image.open(image_path)
        
        # Generate response with safety settings
        response = model.generate_content(
            [prompt, image],
        )
        
        return response.text
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None

def main():
    # Setup Gemini
    model = setup_gemini()
    
    # Image path
    image_path = f"C:/Users/nguye/Desktop/slide_convert/output/cse484-lecture16-25sp.pdf/images/9c868dcaafbd34a49398e914db4eea942b480b1a43fb9343a3c3879e49cb7f75.jpg"
    
    # Custom prompt
    prompt = """
    Analyze this image from a computer security lecture slide. Write a short and concise caption for the image that is use for accessibility (alt text for image).
    """
    
    # Analyze image
    print("Analyzing image...")
    result = analyze_image(model, image_path, prompt)
    
    if result:
        print("/nAnalysis Result:")
        print("-" * 50)
        print(result)
        print("-" * 50)
    else:
        print("Failed to analyze image")

if __name__ == "__main__":
    main()