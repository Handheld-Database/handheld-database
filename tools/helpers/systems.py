import json
import os, sys
from helpers.os import scan_input

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
    
    # Updating the list of systems in platforms/myplatform/index.js
    update_system_list(platform_name, system_name)


# Funtion to update the system list for the platform
def update_system_list(platform_name, system_name_as_key):
    """
    Updates the list of systems with the new added system name and key.

    Parameters:
    platform_name (str): normalized name of the platfrom.
    system_name_as_key (str): normalized name of the system.
    full_system_name (str): The systems full name, the user prompted to define it.
    """

    # Asking the user for the system's full name
    full_system_name = scan_input("What is the system's full name (Nintendo DS or Playstation Portable): ")

    # Platform's index.js path that contains the list of systems. /platforms/myplatformname/index.js
    system_list_index_path = os.path.join('platforms', platform_name, 'index.json')
    system_list = []

    # Reading index.json and storing "systems" attribute.
    if os.path.exists(system_list_index_path):
        with open(system_list_index_path, 'r') as f:
            try:
                data = json.load(f)
                system_list= data.get('systems', [])
                f.close()
            except json.JSONDecodeError:
                system_list = []

    # Construct data which will be added to the list
    system_entry = {
        "name": full_system_name,
        "key": system_name_as_key
    }

    # Check if the to be added system already in the list.
    for item in system_list:
        if(item['key'] == system_entry['key']):
            exist = 1
            break

    # Add the new system to the file and write it, if it does not exists.
    match exit:
        case 1:
            print("---------------------------------")
            print("|  This system already exists in "+ system_name_as_key +"  |")
            print("---------------------------------")
        case _: # default case
            with open(system_list_index_path, 'w') as f:
                data["systems"].append(system_entry)   
                json.dump(data, f, indent = 4)  
                f.close()
                print()
                print("|-->  System added to " + system_name_as_key + "  <--|")
                print()

           

   
