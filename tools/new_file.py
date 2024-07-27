import argparse, sys
from helpers.games import create_game
from helpers.platforms import create_platform
from helpers.systems import create_system
# Function to display help text for using the script
def display_help():
    help_text = """
    Usage: python script.py [command] [arguments] [--steamgrid-key your_api_key]
    
    Commands:
    new platform [platform_name]            Create a new platform
    new system [platform_name] [system_name] Create a new system under a specified platform
    new game [platform_name] [system_name] [game_name] Create a new game under a specified platform and system
    help                                    Display this help message
    
    Examples:
    python script.py new platform myplatform
    python script.py new system myplatform mysystem
    python script.py new game myplatform mysystem mygame
    python script.py new platform myplatform --steamgrid-key myapikey
    python script.py new system myplatform mysystem --steamgrid-key myapikey
    python script.py new game myplatform mysystem mygame --steamgrid-key myapikey
    """
    print(help_text)
# Main function to handle command line arguments and execute corresponding actions
def main():
    parser = argparse.ArgumentParser(description="Game management script")
    parser.add_argument('command', choices=['new', 'help'], help='Command to execute')
    parser.add_argument('entity', nargs='?', choices=['platform', 'system', 'game'], help='Entity type')
    parser.add_argument('names', nargs='*', help='Names for the entity')
    parser.add_argument('--steamgrid-key', help='API key for authentication')

    args = parser.parse_args()

    if args.command == 'help':
        display_help()
    elif args.command == 'new':
        if not args.entity or not args.names:
            display_help()
            sys.exit(1)

        
        api_key = args.steamgrid_key

        if args.entity == 'platform':
            if len(args.names) != 1:
                display_help()
                sys.exit(1)
            platform_name = args.names[0]
            create_platform(platform_name)
        elif args.entity == 'system':
            if len(args.names) != 2:
                display_help()
                sys.exit(1)
            platform_name, system_name = args.names
            create_system(platform_name, system_name)
        elif args.entity == 'game':
            if len(args.names) != 3:
                display_help()
                sys.exit(1)
            platform_name, system_name, game_name = args.names
            create_game(platform_name, system_name, game_name, api_key)
        else:
            print("Unknown entity type. Use 'platform', 'system', or 'game'.")
            display_help()
    else:
        print("Unknown command. Use 'new' or 'help'.")
        display_help()

if __name__ == '__main__':
    main()