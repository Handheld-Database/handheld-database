import json, os, sys, re

# Function to get user input and strip leading/trailing whitespace
def scan_input(prompt):
    return input(prompt).strip()

# Function to get array input from user, split by ';', and strip whitespace
def scan_array_input(prompt):
    return input(prompt).strip().split(';')

# Function to normalize input string by removing extra spaces and non-word characters
def normalize_string(input_string):
    normalized_string = re.sub(r'\s+', ' ', input_string)  # Collapse multiple spaces into one
    normalized_string = re.sub(r'[^\w\s]', '', normalized_string)  # Remove non-word characters
    normalized_string = normalized_string.strip()  # Remove leading/trailing spaces
    return normalized_string

# Function to normalize input string by removing all spaces, non-word characters and lower case
def normalize_string_2(input_string):
    normalized_string = normalize_string(input_string)
    normalized_string = normalized_string.lower()
    normalized_string = re.sub(r'\s+', '', normalized_string)
    return normalized_string

# Function to create a new platform
def create_platform(platform_name_arg):
    attributes = {}

    # Prompting user for platform attributes
    attributes["name"] = scan_input("Enter the name: ")
    attributes["database_key"] = normalize_string_2(scan_input("Enter the database key: "))
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
    update_platforms_list(attributes)

# Function to update the list of platforms in the main index.json
def update_platforms_list(attributes):
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
        "manufacturer": attributes.get("manufacturer", ""),
        "system": attributes.get("system", "")
    }

    platforms_list.append(platform_entry)

    # Write updated platform list back to index.json
    data = {"platforms": platforms_list}

    with open(platforms_list_path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to create a new system under a specified platform
def create_system(platform_name, system_name):
    system_dir = os.path.join('platforms', platform_name, 'systems', system_name)
    os.makedirs(system_dir, exist_ok=True)
    
    # Create index.json for the system
    system_index_path = os.path.join(system_dir, 'index.json')
    if not os.path.exists(system_index_path):
        with open(system_index_path, 'w') as f:
            json.dump({"name": system_name, "games": []}, f, indent=4)

# Function to create a new game under a specified platform and system
def create_game(platform_name, system_name, game_name):

    normalize_game_name = normalize_string_2(game_name)
    normalize_system_name = normalize_string_2(system_name)
    normalize_platform_name = normalize_string_2(platform_name)

    print(normalize_game_name)

    game_dir = os.path.join('platforms', normalize_platform_name, 'systems', normalize_system_name, normalize_game_name)
    os.makedirs(game_dir, exist_ok=True)
    
    attributes = {}

    # Prompt user for game attributes
    attributes["name"] = normalize_string(game_name)
    attributes["key"] = normalize_string_2(game_name)
    attributes["rank"] = scan_input("Enter the rank (GOLD, SILVER, BRONZE & GARBAGE): ")

    # Create json and md files for the game
    game_json_path = os.path.join(game_dir, f'{normalize_game_name}.json')
    if not os.path.exists(game_json_path):
        with open(game_json_path, 'w') as f:
            json.dump(attributes, f, indent=4)
    
    game_md_path = os.path.join(game_dir, f'{normalize_game_name}.md')
    if not os.path.exists(game_md_path):
        with open(game_md_path, 'w') as f:
            f.write(f'# {game_name}\n\nDetailed description of the game.')

    update_games_list(normalize_platform_name, normalize_system_name, attributes)

# Function to update the list of platforms in the main index.json
def update_games_list(platform_name, system_name, attributes):
    games_list = []
    
    games_list_path = os.path.join('platforms', platform_name, 'systems', system_name, 'index.json')
    if os.path.exists(games_list_path):
        with open(games_list_path, 'r') as f:
            try:
                data = json.load(f)
                games_list = data.get('games', [])
            except json.JSONDecodeError:
                games_list = []
    
    # Extract relevant attributes for the platform entry
    game_entry = {
        "name": attributes["name"],
        "key": attributes["key"],
        "rank": attributes["rank"],
    }

    games_list.append(game_entry)

    # Write updated platform list back to index.json
    data = {"games": games_list}

    with open(games_list_path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display help text for using the script
def display_help():
    help_text = """
    Usage: python script.py [command] [arguments]
    
    Commands:
    new platform [platform_name]            Create a new platform
    new system [platform_name] [system_name] Create a new system under a specified platform
    new game [platform_name] [system_name] [game_name] Create a new game under a specified platform and system
    help                                    Display this help message
    
    Examples:
    python script.py new platform myplatform
    python script.py new system myplatform mysystem
    python script.py new game myplatform mysystem mygame
    """
    print(help_text)

# Main function to handle command line arguments and execute corresponding actions
def main():
    if len(sys.argv) < 2:
        display_help()
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'new':
        if len(sys.argv) < 4:
            display_help()
            sys.exit(1)
        entity = sys.argv[2]
        if entity == 'platform':
            if len(sys.argv) != 4:
                display_help()
                sys.exit(1)
            platform_name = sys.argv[3]
            create_platform(platform_name)
        elif entity == 'system':
            if len(sys.argv) != 5:
                display_help()
                sys.exit(1)
            platform_name = sys.argv[3]
            system_name = sys.argv[4]
            create_system(platform_name, system_name)
        elif entity == 'game':
            if len(sys.argv) != 6:
                display_help()
                sys.exit(1)
            platform_name = sys.argv[3]
            system_name = sys.argv[4]
            game_name = sys.argv[5]
            create_game(platform_name, system_name, game_name)
        else:
            print("Unknown entity type. Use 'platform', 'system', or 'game'.")
            display_help()
    elif action == 'help':
        display_help()
    else:
        print("Unknown action. Use 'new' or 'help'.")
        display_help()

if __name__ == '__main__':
    main()