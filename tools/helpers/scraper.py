import requests
from bs4 import BeautifulSoup

def _get_game_url(game_name, platform):
    """
    Searches for a game on MobyGames and returns the URL of the game's page
    for the specified platform.

    Parameters:
    game_name (str): The name of the game to search for.
    platform (str): The platform to filter the search results by.

    Returns:
    str: The URL of the game's page on MobyGames if found, None otherwise.
    """
    search_url = f"https://www.mobygames.com/search/?q={game_name}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the search results table
    table = soup.find('table', class_='table mb')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            # Get the game link and game name from the row
            game_link_tag = row.find('a', href=True)
            game_name_tag = row.find('b').find('a')
            if game_name_tag and game_name.lower() in game_name_tag.get_text(strip=True).lower():
                # Check if the game is available for the specified platform
                platform_tags = row.find_all('small')
                for platform_tag in platform_tags:
                    if platform in platform_tag.get_text(strip=True):
                        game_link = game_link_tag['href']
                        return game_link
    
    return None

def get_game_description(game_name, platform):
    """
    Fetches and returns the description of a game from its MobyGames page.

    Returns:
    str: The description of the game if found, an empty string otherwise.
    """
    game_url = _get_game_url(game_name, platform)
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the description div on the game page
    description_div = soup.find('div', id='description-text')
    if description_div:
        paragraphs = description_div.find_all('p')
        description_parts = []
        for p in paragraphs:
            parts = []
            for content in p.contents:
                # Collect text from each paragraph
                parts.append(content.get_text(strip=True))
            description_parts.append(' '.join(parts))
        description = ' '.join(description_parts)
        return description.strip()
    
    return ""
