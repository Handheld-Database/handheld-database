from bs4 import BeautifulSoup
import csv, argparse, os, json, re, requests
from PIL import Image
from io import BytesIO
from igdb.wrapper import IGDBWrapper

def get_game_url(game_name, platform):
    search_url = f"https://www.mobygames.com/search/?q={game_name}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='table mb')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            game_link_tag = row.find('a', href=True)
            game_name_tag = row.find('b').find('a')
            if game_name_tag and game_name.lower() in game_name_tag.get_text(strip=True).lower():
                platform_tags = row.find_all('small')
                for platform_tag in platform_tags:
                    if platform in platform_tag.get_text(strip=True):
                        game_link = game_link_tag['href']
                        return game_link
    
    return None

def get_game_description(game_url):
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    description_div = soup.find('div', id='description-text')
    if description_div:
        paragraphs = description_div.find_all('p')
        description_parts = []
        for p in paragraphs:
            parts = []
            for content in p.contents:
                parts.append(content.get_text(strip=True))
            description_parts.append(' '.join(parts))
        description = ' '.join(description_parts)
        return description.strip()

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

# Function to extract the clean game name
def extract_game_name(filename):
    # Remove file extension
    filename = re.sub(r'\.zip$', '', filename)
    # Remove region codes, [!], and other parenthetical content
    filename = re.sub(r'\s*\(.*?\)\s*', '', filename)
    filename = re.sub(r'\s*\[!\]\s*', '', filename)
    return filename.strip()

# Simulating scan_input function for rank
def scan_input(prompt):
    return input(prompt)

# Main function to create games
def create_game(platform_name, system_name, game_name, rank, observations):
    normalize_game_name = normalize_string_2(game_name)
    normalize_system_name = normalize_string_2(system_name)
    normalize_platform_name = normalize_string_2(platform_name)

    game_dir = os.path.join('platforms', normalize_platform_name, 'systems', normalize_system_name, normalize_game_name)
    os.makedirs(game_dir, exist_ok=True)
    
    attributes = {
        "name": normalize_string(game_name),
        "key": normalize_string_2(game_name),
        "rank": rank
    }

    # Create JSON file for the game
    game_json_path = os.path.join(game_dir, f'{normalize_game_name}.json')
    if not os.path.exists(game_json_path):
        with open(game_json_path, 'w') as f:
            json.dump(attributes, f, indent=4)

    MARKDOWN = f'''# {game_name} \n\n%game_overview%\n\n## Execution information\n\n'''
    
    # Create Markdown file for the game
    game_md_path = os.path.join(game_dir, f'{normalize_game_name}.md')
    if not os.path.exists(game_md_path):
        with open(game_md_path, 'w') as f:
            f.write(MARKDOWN)
            f.write('\n'.join(observations))

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
        "rank": attributes["rank"]
    }

    games_list.append(game_entry)

    # Write updated platform list back to index.json
    data = {"games": games_list}

    with open(games_list_path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to fetch image game id from SteamGridDB
def fetch_steamgriddb_game_id(api_key, game_name):
    base_url = f'https://www.steamgriddb.com/api/v2/search/autocomplete/'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        response = requests.get(f'{base_url}{game_name}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            if(len(data['data']) > 0):
                return data['data'][0]['id']
        else:
            print(f"Error fetching data for {game_name}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


# Função para buscar URLs de imagens do SteamGridDB
def fetch_steamgriddb_game_urls(api_key, game_id):
    base_url = f'https://www.steamgriddb.com/api/v2/grids/game/'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        response = requests.get(f'{base_url}{game_id}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            image_urls = {'square': None, 'rectangular': None}

            images_list = data['data']
            
            # Filtrar imagens quadradas e retangulares
            square_images = list(filter(lambda x: x['style'] == 'alternate' and x['width'] == x['height'], images_list))
            rectangular_images = list(filter(lambda x: x['style'] == 'alternate' and x['width'] > x['height'], data['data']))
            
            # Selecionar a primeira imagem de cada tipo, se existirem
            if square_images:
                image_urls['square'] = square_images[0]['url']
            if rectangular_images:
                image_urls['rectangular'] = rectangular_images[0]['url']
            
            return image_urls
        else:
            print(f"No data found for game ID {game_id}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def download_and_convert_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        # Remove alpha channel by converting to RGB
        image = image.convert("RGB")
        # Save the image in WebP format with quality 70
        image.save(save_path, 'WEBP', quality=70 )
    else:
        print(f"Failed to download image from {image_url}")

# Argument parser setup
parser = argparse.ArgumentParser(description='Process a CSV file of game data.')
parser.add_argument('csv_file', type=str, help='The path to the CSV file to process.')
parser.add_argument('steamgrid_key', type=str, help='The Steamgriddb API key.')
args = parser.parse_args()

# Read CSV data from file
csv_file_path = args.csv_file
steam_grid_api_key = args.steamgrid_key
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader)
    for row in csvreader:
        if len(row) == 0:
            continue
        game_name = extract_game_name(row[1])
        observations = [
            f"### Tested on RA 1.18.0 Crossmix 1.1.0 Performance mode"
            f"\n\n**RA ParaLLEl Dynarec/Gln64**: {row[3] if len(row[3]) > 1 else 'Not tested'}",
            f"\n**RA Mupen Pure/HLE**: {row[4] if len(row[4]) > 1 else 'Not tested'}",
            f"\n**RA ParaLLEl Dynarec/Rice**: {row[5] if len(row[5]) > 1 else 'Not tested'}",
            f"\n**RA Mupen Dynarec/HLE**: {row[6] if len(row[6]) > 1 else 'Not tested'}",
            F"\n**Recommended Core config**: {row[2] if len(row[2]) > 1 else 'Not tested'}"
            f"\n**Notes**: {row[7]}" if len(row[7]) > 0 else None,
        ]
        observations = [obs for obs in observations if obs]  # Remove empty observations

        print("tsp", "n64", game_name, observations)

        game_id = fetch_steamgriddb_game_id(steam_grid_api_key, game_name)

        # Determine rank
        rank = "FAULTY"
        if "P" in row[0]:
            rank = "PLATINUM"
        elif "G" in row[0]:
            rank = "GOLD"
        elif "S" in row[0]:
            rank = "SILVER"
        elif "B" in row[0]:
            rank = "BRONZE"
        elif "F" in row[0]:
            rank = "FAULTY"

        print(steam_grid_api_key, game_id)

        icon_url = ""
        cover_url = ""
        normalize_game_name = normalize_string_2(game_name)

        if game_id is not None:
            image_urls = fetch_steamgriddb_game_urls(steam_grid_api_key, game_id)
            icon_url = image_urls['square']
            cover_url = image_urls['rectangular']

        # Download and convert images
        game_folder = os.path.join("commons", "images", "games")
        os.makedirs(game_folder, exist_ok=True)
        if cover_url:
            cover_save_path = os.path.join(game_folder, f'{normalize_game_name}.cover.webp')
            download_and_convert_image(cover_url, cover_save_path)
        if icon_url:
            icon_save_path = os.path.join(game_folder, f'{normalize_game_name}.icon.webp')
            download_and_convert_image(icon_url, icon_save_path)

        game_url = get_game_url(game_name, "Nintendo 64")
        if game_url:
            print(f"Game URL: {game_url}")
            game_description = get_game_description(game_url)
            if game_description:
                print("Game Description:")
                print(game_description)
                MD_OVERVIEW = f"## Overview\n\n{game_description}"
                game_md_path = os.path.join("commons", "overviews", f'{normalize_game_name}.overview.md')
                if not os.path.exists(game_md_path):
                    with open(game_md_path, 'w') as f:
                        f.write(MD_OVERVIEW)
            else:
                print("Description not found.")
        else:
            print("Game not found on Nintendo 64 platform.")
            
        # Create the game with parsed data
        create_game("tsp", "n64", game_name, rank, observations)
