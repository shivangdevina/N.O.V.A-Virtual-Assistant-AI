import os
import asyncio
from random import randint
from PIL import Image
from dotenv import get_key
from time import sleep
from huggingface_hub import InferenceClient  # Requires huggingface_hub package

# Set API key from .env file
try:
    api_key = get_key('.env', 'HuggingFaceAPIKey')
    if api_key:
        os.environ["HF_TOKEN"] = api_key
    else:
        print("Warning: HuggingFaceAPIKey not found in .env file")
        print("Please add HuggingFaceAPIKey=your_api_key to your .env file")
except Exception as e:
    print(f"Error loading HuggingFace API key: {e}")
    print("Please check your .env file contains: HuggingFaceAPIKey=your_api_key")

def open_images(prompt):
    folder_path = r"Data"
    prompt_clean = prompt.replace(" ", "_")
    
    # Create directory if needed
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    files = [f"{prompt_clean}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Async function to generate a single image
async def generate_single_image(prompt, index):
    try:
        # Check if API key is available
        if not os.environ.get("HF_TOKEN"):
            print("Error: HuggingFace API key not available")
            return None
            
        # Create client for each request to ensure thread safety
        client = InferenceClient(
            provider="nscale",
            api_key=os.environ["HF_TOKEN"]
        )
        
        # Generate image with random seed
        seed = randint(0, 1000000)
        print(f"Generating image {index} for prompt: {prompt}")
        
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
            seed=seed
        )
        
        # Save the image
        prompt_clean = prompt.replace(" ", "_")
        filename = f"Data/{prompt_clean}{index}.jpg"
        image.save(filename)
        print(f"Saved image: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error generating image {index}: {str(e)}")
        return None

async def generate_images(prompt: str):
    # Create output directory
    if not os.path.exists("Data"):
        os.makedirs("Data")
    
    print(f"Starting image generation for: {prompt}")
    
    # Create tasks for 4 images
    tasks = [generate_single_image(prompt, i+1) for i in range(4)]
    
    # Run tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Count successful generations
    successful = sum(1 for result in results if result is not None and not isinstance(result, Exception))
    print(f"Successfully generated {successful} out of 4 images")
    
    # Return success status
    return successful > 0

def GenerateImages(prompt: str):
    print(f"Generating images for: {prompt}")
    success = asyncio.run(generate_images(prompt))
    
    if success:
        open_images(prompt)
    else:
        print("Failed to generate any images")

# Main monitoring loop
def main():
    print("Image Generation Service Started")
    print("Waiting for image generation requests...")
    
    while True:
        try:
            # Check for image generation requests
            data_file = r"Frontend\Files\ImageGeneration.data"
            
            # Check if file exists
            if not os.path.exists(data_file):
                sleep(1)
                continue
            
            with open(data_file, "r") as f:
                data = f.read().strip()
            
            if not data:
                sleep(1)
                continue
                
            parts = data.split(',', 1)
            if len(parts) < 2:
                sleep(1)
                continue
                
            prompt = parts[0].strip()
            status = parts[1].strip()
            
            if status == "True":
                print(f"Processing image generation request: {prompt}")
                GenerateImages(prompt)
                
                # Reset status
                with open(data_file, "w") as f:
                    f.write("False,False")
                print("Image generation completed")
                break
                
            sleep(1)
            
        except Exception as e:
            print(f"Main loop error: {str(e)}")
            sleep(1)

if __name__ == "__main__":
    main()