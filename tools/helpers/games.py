import json
import os
from helpers.images import download_game_images
from helpers.os import scan_input
from helpers.scraper import get_game_description
from helpers.steamgrid import SteamGridDB
from helpers.strings import normalize_string_lower
from helpers.templates import generate_game_templates_md


def create_game(platform_name, system_name, game_name, tester, api_key=None):
    """
    Creates a directory structure and necessary files for a game under the specified platform and system.

    Parameters:
    platform_name (str): The name of the platform.
    system_name (str): The name of the system.
    game_name (str): The name of the game.
    api_key (str, optional): The API key for SteamGridDB. Default is None.
    """
    normalized_platform_name, normalized_system_name, normalized_game_name = map(normalize_string_lower, 
                                                                                [platform_name, system_name, game_name])

    game_dir = os.path.join('platforms', normalized_platform_name, 'systems', normalized_system_name, normalized_game_name)
    os.makedirs(game_dir, exist_ok=True)

    attributes = gather_game_attributes(game_name)
    
    platform_moby = scan_input("Enter the platform name (PSP, Nintendo 64, check https://www.mobygames.com/platform/): ")
    description = get_game_description(game_name, platform_moby)

    if api_key:
        download_images(api_key, game_name, normalized_game_name)
        
    create_game_files(game_dir, game_name, system_name, attributes, description)

def gather_game_attributes(game_name):
    """
    Gathers game attributes from the user.

    Parameters:
    game_name (str): The name of the game.

    Returns:
    dict: A dictionary containing the game attributes.
    """
    return {
        "name": game_name,
        "key": normalize_string_lower(game_name)
    }

def download_images(api_key, game_name, normalized_game_name):
    """
    Fetches game image URLs and downloads images.

    Parameters:
    api_key (str): The API key for SteamGridDB.
    game_name (str): The name of the game.
    normalized_game_name (str): The normalized game name.
    """
    image_urls = SteamGridDB(api_key).get_game_image_urls(game_name)
    if image_urls:
        download_game_images(image_urls.get('rectangular'), image_urls.get('square'), normalized_game_name)

def create_game_files(game_dir, game_name, system_name, attributes, description):
    """
    Creates the necessary JSON and Markdown files for the game.

    Parameters:
    game_dir (str): The directory where the game files will be created.
    game_name (str): The name of the game.
    system_name (str): The name of the system.
    attributes (dict): A dictionary containing the game attributes.
    description (str): The description of the game.
    """
    normalized_game_name = normalize_string_lower(game_name)
    create_json_file(game_dir, normalized_game_name, attributes)
    create_markdown_file(game_dir, game_name, system_name)
    create_overview_file(normalized_game_name, game_name, description)

def create_json_file(game_dir, normalized_game_name, attributes):
    """
    Creates a JSON file for the game.

    Parameters:
    game_dir (str): The directory where the game files will be created.
    normalized_game_name (str): The normalized game name.
    attributes (dict): A dictionary containing the game attributes.
    """
    game_json_path = os.path.join(game_dir, f'{normalized_game_name}.json')
    if not os.path.exists(game_json_path):
        with open(game_json_path, 'w') as f:
            json.dump(attributes, f, indent=4)       

def create_markdown_file(game_dir, game_name, system_name):
    """
    Creates a Markdown file for the game.

    Parameters:
    game_dir (str): The directory where the game files will be created.
    game_name (str): The name of the game.
    system_name (str): The name of the system.
    """
    game_md_path = os.path.join(game_dir, f'{normalize_string_lower(game_name)}.md')
    if not os.path.exists(game_md_path):
        with open(game_md_path, 'w') as f:
            game_template = generate_game_templates_md(game_name, normalize_string_lower(system_name))
            f.write(game_template)
   

def create_overview_file(normalized_game_name, game_name, description):
    """
    Creates an overview Markdown file for the game.

    Parameters:
    normalized_game_name (str): The normalized game name.
    game_name (str): The name of the game.
    description (str): The description of the game.
    """
    game_overview_path = os.path.join('commons', 'overviews', f'{normalized_game_name}.overview.md')
    if not os.path.exists(game_overview_path):
        with open(game_overview_path, 'w') as f:
            f.write(f'## Overview\n\n{description}\n\n# KEY INFORMATION\n\n- **Developer**:\n- **Publisher**:\n- **Platforms**:\n- **Release Date**:\n- **Genre**:\n- **Modes**:\n\n# Source of information\n FOR EXAMPLE: WIKIPEDIA: [LINK](LINK TO THE SOURCE)')