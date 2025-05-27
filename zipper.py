import requests
import os
import zipfile
from urllib.parse import urlparse
from pathlib import Path

def download_and_extract_zip(zip_url, custom_base_name = None):
    # Create output directory if it doesn't exist
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Get filename from URL
    parsed_url = urlparse(zip_url)
    zip_filename = os.path.basename(parsed_url.path)
    base_name = os.path.splitext(zip_filename)[0]

    if custom_base_name:
        extract_dir = output_dir / custom_base_name
    else:
        # Create specific directory for this zip
        extract_dir = output_dir / base_name
    extract_dir.mkdir(exist_ok=True)
    
    try:
        # Download the zip file
        print(f"Downloading {zip_url}...")
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
        
        # Save zip file temporarily
        temp_zip = output_dir / zip_filename
        with open(temp_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the zip file
        print(f"Extracting to {extract_dir}...")
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Remove the temporary zip file
        temp_zip.unlink()
        
        print(f"Successfully extracted to {extract_dir}")
        return extract_dir
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
    except zipfile.BadZipFile:
        print("Error: The file is not a valid ZIP file")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python zip.py <zip_url>")
        sys.exit(1)
    
    zip_url = sys.argv[1]
    download_and_extract_zip(zip_url) 