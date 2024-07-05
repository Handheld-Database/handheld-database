import json
import os

# Function to create a new system under a specified platform
def create_system(platform_name, system_name):
    """
    Creates a new system under a specified platform by creating the necessary directory structure and an index.json file.

    Parameters:
    platform_name (str): The name of the platform under which the system will be created.
    system_name (str): The name of the system to be created.
    """
    # Define the directory path for the new system
    system_dir = os.path.join('platforms', platform_name, 'systems', system_name)
    # Create the directory if it does not exist
    os.makedirs(system_dir, exist_ok=True)
    
    # Define the path for the system's index.json file
    system_index_path = os.path.join(system_dir, 'index.json')
    if not os.path.exists(system_index_path):
        # Create and write the initial JSON structure to index.json
        with open(system_index_path, 'w') as f:
            json.dump({"name": system_name, "games": []}, f, indent=4)