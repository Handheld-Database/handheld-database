import csv, argparse, os

from helpers.games import create_game
from helpers.images import download_game_images
from helpers.scraper import get_game_description
from helpers.steamgrid import SteamGridDB
from helpers.strings import extract_game_name, normalize_string_lower

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
        game_name = extract_game_name(row[0])
        observations = [
            f"**Tester**: {row[1] if len(row[1]) > 1 else 'Not tested'}",
            f"**Backend**: {row[3] if len(row[3]) > 1 else 'Not tested'}",
            f"**Resolution**: {row[2] if len(row[2]) > 1 else 'Not tested'}",
            f"**Notes**: {row[5]}" if len(row[5]) > 0 else None

        ]
        observations = [obs for obs in observations if obs]  # Remove empty observations

        print("tsp", "psp", game_name, observations)

        # Determine rank
        rank = row[4]

        icon_url = ""
        cover_url = ""
        normalize_game_name = normalize_string_lower(game_name)


        if normalize_game_name is not None:
            image_urls = SteamGridDB(steam_grid_api_key).get_game_image_urls(game_name)
            icon_url = image_urls['square']
            cover_url = image_urls['rectangular']

        # Download and convert images
        download_game_images(cover_url, image_urls, normalize_game_name)

        game_description = get_game_description(game_name, "PSP")
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
            
        # Create the game with parsed data
        create_game("tsp", "psp", game_name, rank, observations)
