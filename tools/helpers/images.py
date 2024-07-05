from io import BytesIO
import os
import requests
from PIL import Image

# Function to download and convert images
def _download_and_convert_image(image_url, save_path):
    """
    Downloads an image from the provided URL, converts it to RGB format, and saves it as a WebP file.

    Parameters:
    image_url (str): The URL of the image to download.
    save_path (str): The local file path to save the converted image.
    """
    
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        # Remove alpha channel by converting to RGB
        image = image.convert("RGB")
        # Save the image in WebP format with quality 70
        image.save(save_path, 'WEBP', quality=70)
    else:
        print(f"Failed to download image from {image_url}")

# Function to download game cover and icon images
def download_game_images(cover_url, icon_url, normalize_game_name):
    """
    Downloads and converts game cover and icon images, and saves them in the specified format and directory.

    Parameters:
    cover_url (str): The URL of the cover image to download.
    icon_url (str): The URL of the icon image to download.
    normalize_game_name (str): The normalized game name to use in the saved file names.
    """
    game_folder = os.path.join("commons", "images", "games")
    os.makedirs(game_folder, exist_ok=True)
    
    if cover_url:
        cover_save_path = os.path.join(game_folder, f'{normalize_game_name}.cover.webp')
        _download_and_convert_image(cover_url, cover_save_path)
    
    if icon_url:
        icon_save_path = os.path.join(game_folder, f'{normalize_game_name}.icon.webp')
        _download_and_convert_image(icon_url, icon_save_path)
