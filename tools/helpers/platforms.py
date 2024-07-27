import json
import os

from helpers.os import scan_array_input, scan_input
from helpers.strings import normalize_string, normalize_string_lower
# Function to create a new platform
def create_platform(platform_name_arg):
    """
    Creates a new platform by prompting the user for various attributes and saving the information in a JSON file.

    Parameters:
    platform_name_arg (str): The name of the platform to be created.
    """
    attributes = {}

    # Prompting user for platform attributes
    attributes["name"] = scan_input("Enter the name: ")
    attributes["database_key"] = normalize_string_lower(scan_input("Enter the database key: "))
    attributes["manufacturer"] = scan_input("Enter the manufacturer: ")
    attributes["screen_size"] = scan_input("Enter the screen size: ")
    attributes["resolution"] = scan_input("Enter the resolution: ")
    attributes["battery_life"] = scan_input("Enter the battery life: ")
    attributes["weight"] = scan_input("Enter the weight: ")
    attributes["system"] = scan_input("Enter the system: ")
    attributes["cpu"] = scan_input("Enter the CPU: ")
    attributes["gpu"] = scan_input("Enter the GPU: ")
    attributes["ram"] = scan_input("Enter the RAM: ")
    attributes["arch"] = scan_input("Enter the architecture: ")
    attributes["storage"] = scan_input("Enter the storage: ")
    attributes["media"] = scan_input("Enter media: ")
    attributes["connectivity"] = scan_array_input("Enter connectivity (separate with ';'): ")
    attributes["systems"] = [{"name": "Name", "key": "key"}]

    # Normalize platform name to use as directory name
    platform_name = normalize_string(platform_name_arg)
    platform_dir = os.path.join('platforms', platform_name)
    os.makedirs(platform_dir, exist_ok=True)

    # Create index.json for the platform
    platform_index_path = os.path.join(platform_dir, 'index.json')
    if not os.path.exists(platform_index_path):
        with open(platform_index_path, 'w') as f:
            json.dump(attributes, f, indent=4)
    
    # Update the list of platforms in the main index.json
    update_platforms_list(attributes, platform_name)
# Function to update the list of platforms in the main index.json
def update_platforms_list(attributes, platform_name):
    """
    Updates the main index.json file to include the newly created platform.

    Parameters:
    attributes (dict): The attributes of the newly created platform.
    platform_name: normalized platform name, for setting the image path
    """
    platforms_list = []
    
    platforms_list_path = os.path.join('platforms', 'index.json')
    if os.path.exists(platforms_list_path):
        with open(platforms_list_path, 'r') as f:
            try:
                data = json.load(f)
                platforms_list = data.get('platforms', [])
            except json.JSONDecodeError:
                platforms_list = []
    
    # Extract relevant attributes for the platform entry
    platform_entry = {
        "name": attributes["name"],
        "database_key": attributes["database_key"],
        "image": ("platforms/"+ platform_name + ".webp"),
        "manufacturer": attributes.get("manufacturer", ""),
        "system": attributes.get("system", "")
    }

    platforms_list.append(platform_entry)

    # Write updated platform list back to index.json
    data = {"platforms": platforms_list}

    with open(platforms_list_path, 'w') as f:
        json.dump(data, f, indent=4)