# resize.py
from PIL import Image
import os

# Specify the target folder path
folder_path = os.getcwd()  # get current directory
max_file_size = 100 * 1024  # 100 KB

def resize_image(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
        # Start with an initial resize factor
        resize_factor = 0.9
        while os.path.getsize(file_path) > max_file_size:
            # Calculate new size
            new_width = int(width * resize_factor)
            new_height = int(height * resize_factor)
            # Resize the image
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)  # Updated from ANTIALIAS to LANCZOS
            # Save the resized image to overwrite the original
            img_resized.save(file_path, format="PNG", optimize=True)
            # Update dimensions for further resizing, if needed
            width, height = img_resized.size
            # Decrease the resize factor
            resize_factor -= 0.05
            # Close the resized image
            img_resized.close()

def resize_all_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > max_file_size:
                    print(f"Resizing {file_path}...")
                    resize_image(file_path)

if __name__ == "__main__":
    resize_all_images(folder_path)