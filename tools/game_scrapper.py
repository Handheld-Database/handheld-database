import requests
from bs4 import BeautifulSoup

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


game_name = "Mario Kart 64"
platform = "Nintendo 64"
game_url = get_game_url(game_name, platform)
if game_url:
    print(f"Game URL: {game_url}")
    game_description = get_game_description(game_url)
    if game_description:
        print("Game Description:")
        print(game_description)
    else:
        print("Description not found.")
else:
    print("Game not found on Nintendo 64 platform.")
