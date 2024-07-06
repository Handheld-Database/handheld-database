import json
import os
from helpers.images import download_game_images
from helpers.os import scan_input
from helpers.scraper import get_game_description
from helpers.steamgrid import SteamGridDB
from helpers.strings import normalize_string_lower
from helpers.templates import generate_game_templates_md

def create_game(platform_name, system_name, game_name, api_key=None):
    """
    Creates a directory structure and necessary files for a game under the specified platform and system.

    Parameters:
    platform_name (str): The name of the platform.
    system_name (str): The name of the system.
    game_name (str): The name of the game.
    """
    normalized_game_name = normalize_string_lower(game_name)
    normalized_system_name = normalize_string_lower(system_name)
    normalized_platform_name = normalize_string_lower(platform_name)

    game_dir = os.path.join('platforms', normalized_platform_name, 'systems', normalized_system_name, normalized_game_name)
    os.makedirs(game_dir, exist_ok=True)

    attributes = gather_game_attributes(game_name)
    
    # Fetch game description and add to attributes
    platform_moby = scan_input("Enter the platform name (PSP, Nintendo 64, check https://www.mobygames.com/platform/): ")
    description = get_game_description(game_name, platform_moby)

    # Fetch game image URLs and download images
    if(api_key):
        image_urls = SteamGridDB(api_key).get_game_image_urls(game_name)
        if image_urls:
            download_game_images(image_urls.get('rectangular'), image_urls.get('square'), normalized_game_name)

    create_game_files(game_dir, normalized_game_name, game_name, attributes, description)
    update_games_list(normalized_platform_name, normalized_system_name, attributes)

def gather_game_attributes(game_name):
    """
    Gathers game attributes from the user.

    Parameters:
    game_name (str): The name of the game.

    Returns:
    dict: A dictionary containing the game attributes.
    """
    attributes = {
        "name": game_name,
        "key": normalize_string_lower(game_name),
        "rank": scan_input("Enter the rank (PLATINUM, GOLD, SILVER, BRONZE & FAULTY): ")
    }
    return attributes

def create_game_files(game_dir, normalized_game_name, game_name, attributes, description):
    """
    Creates the necessary JSON and Markdown files for the game.

    Parameters:
    game_dir (str): The directory where the game files will be created.
    normalized_game_name (str): The normalized game name.
    game_name (str): The name of the game.
    attributes (dict): A dictionary containing the game attributes.
    """
    create_json_file(game_dir, normalized_game_name, attributes)
    create_markdown_file(game_dir, normalized_game_name, game_name)
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
    normalized_game_name (str): The normalized game name.
    game_name (str): The name of the game.
    """
    normalized_game_name = normalize_string_lower(game_name)
    game_md_path = os.path.join(game_dir, f'{normalized_game_name}.md')
    if not os.path.exists(game_md_path):
        with open(game_md_path, 'w') as f:
            game_template = generate_game_templates_md(game_name, system_name)
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
            f.write(f'# {game_name}\n\n{description}\n\n# KEY INFORMATION')

def update_games_list(platform_name, system_name, attributes):
    """
    Updates the list of games in the main index.json for a platform.

    Parameters:
    platform_name (str): The name of the platform.
    system_name (str): The name of the system.
    attributes (dict): A dictionary containing game attributes.
    """
    games_list = load_games_list(platform_name, system_name)

    game_entry = {
        "name": attributes["name"],
        "key": attributes["key"],
        "rank": attributes["rank"],
    }

    games_list.append(game_entry)

    save_games_list(platform_name, system_name, games_list)

def load_games_list(platform_name, system_name):
    """
    Loads the list of games from the main index.json for a platform.

    Parameters:
    platform_name (str): The name of the platform.
    system_name (str): The name of the system.

    Returns:
    list: A list of games.
    """
    games_list_path = os.path.join('platforms', platform_name, 'systems', system_name, 'index.json')
    if os.path.exists(games_list_path):
        with open(games_list_path, 'r') as f:
            try:
                data = json.load(f)
                return data.get('games', [])
            except json.JSONDecodeError:
                return []
    return []

def save_games_list(platform_name, system_name, games_list):
    """
    Saves the list of games to the main index.json for a platform.

    Parameters:
    platform_name (str): The name of the platform.
    system_name (str): The name of the system.
    games_list (list): A list of games.
    """
    games_list_path = os.path.join('platforms', platform_name, 'systems', system_name, 'index.json')
    data = {"games": games_list}
    with open(games_list_path, 'w') as f:
        json.dump(data, f, indent=4)