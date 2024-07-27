import os
import json
# Dictionary to map ranks to numeric values
rank_values = {
    "PLATINUM": 5,
    "GOLD": 4,
    "SILVER": 3,
    "BRONZE": 2,
    "FAULTY": 1
}
# Inverse dictionary to map numeric values to ranks
inverse_rank_values = {v: k for k, v in rank_values.items()}

def get_rank_text(average):
    """Determines the textual rank based on the average value."""
    return inverse_rank_values.get(round(average), "UNKNOWN")

def process_md_file(md_path):
    """Processes a .md file to extract ranks and testers."""
    rank_numbers = []
    testers = set()

    with open(md_path, 'r') as md_file:
        lines = md_file.readlines()
        for line in lines:
            if line.startswith("**Rank**"):
                rank_text = line.split(":")[1].strip().upper()
                if rank_text in rank_values:
                    rank_numbers.append(rank_values[rank_text])
                else:
                    print(f"  Unknown rank found: {rank_text}")
            elif line.startswith("**Tester**"):
                tester_name = line.split(":")[1].strip()
                testers.add(tester_name)
    
    return rank_numbers, testers

def update_game_json(json_path, average_rank_numeric, average_rank_text, testers):
    """Updates the JSON file with the average rank and the list of testers."""
    with open(json_path, 'r') as json_file:
        game_data = json.load(json_file)
    
    game_data["rank_numeric"] = round(average_rank_numeric, 2)
    game_data["rank"] = average_rank_text
    game_data["testers"] = list(testers)
    
    with open(json_path, 'w') as json_file:
        json.dump(game_data, json_file, indent=4)
    
    return {
        "name": game_data["name"],
        "key": game_data["key"],
        "rank": average_rank_text
    }

def process_console(console_path):
    """Processes all games in a console."""
    games_list = []

    for game_dir in os.listdir(console_path):
        game_path = os.path.join(console_path, game_dir)
        if os.path.isdir(game_path):
            json_path = os.path.join(game_path, f"{game_dir}.json")
            
            if os.path.exists(json_path):
                rank_numbers = []
                testers = set()

                for file_name in os.listdir(game_path):
                    if file_name.endswith(".md"):
                        md_path = os.path.join(game_path, file_name)
                        print(f"  Processing file {md_path}...")
                        file_rank_numbers, file_testers = process_md_file(md_path)
                        rank_numbers.extend(file_rank_numbers)
                        testers.update(file_testers)
                
                if rank_numbers:
                    average_rank_numeric = sum(rank_numbers) / len(rank_numbers)
                    average_rank_text = get_rank_text(average_rank_numeric)
                    game_info = update_game_json(json_path, average_rank_numeric, average_rank_text, testers)
                    games_list.append(game_info)
                else:
                    print(f"  No rank found in the .md files of folder {game_dir}")

    return games_list

def index_platform(base_path):
    if not os.path.isdir(base_path):
        print(f"The base directory {base_path} does not exist.")
        exit(1)

    for console in os.listdir(base_path):
        console_path = os.path.join(base_path, console)
        if os.path.isdir(console_path):
            print(f"Processing console: {console}")
            games_list = process_console(console_path)
            
            index_path = os.path.join(console_path, 'index.json')
            with open(index_path, 'w') as index_file:
                json.dump({"games": games_list}, index_file, indent=4)
            
            print(f"Index created for the console: {console}")

    print("Processing completed.")

def main():
    base_path = "platforms"
    for platform in os.listdir(base_path):
        platform_path = os.path.join(base_path, platform, 'systems')
        if os.path.isdir(platform_path):
            print(f"Processing platform: {platform}")
            games_list = index_platform(platform_path)
            
            print(f"Platform {platform} processed")

if __name__ == "__main__":
    main()
