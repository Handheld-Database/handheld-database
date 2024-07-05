import requests

class SteamGridDB:
    def __init__(self, api_key):
        """
        Initializes the SteamGridDB class with the provided API key.

        Parameters:
        api_key (str): The API key for accessing the SteamGridDB API.
        """
        self.api_key = api_key
        self.base_url_search = 'https://www.steamgriddb.com/api/v2/search/autocomplete/'
        self.base_url_grids = 'https://www.steamgriddb.com/api/v2/grids/game/'
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def _fetch_game_id(self, game_name):
        """
        Fetches the game ID from SteamGridDB using the game name.

        Parameters:
        game_name (str): The name of the game to search for.

        Returns:
        int: The game ID if found, None otherwise.
        """
        try:
            response = requests.get(f'{self.base_url_search}{game_name}', headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()

            if data.get('data'):
                return data['data'][0]['id']
            else:
                print(f"No game found for {game_name}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def _fetch_game_urls(self, game_id):
        """
        Fetches URLs of square and rectangular images for the game from SteamGridDB.

        Parameters:
        game_id (int): The ID of the game.

        Returns:
        dict: A dictionary containing URLs of square and rectangular images if found, None otherwise.
        """
        try:
            response = requests.get(f'{self.base_url_grids}{game_id}', headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            image_urls = {'square': None, 'rectangular': None}

            images_list = data['data']
            
            # Filter square and rectangular images
            square_images = list(filter(lambda x: x['style'] == 'alternate' and x['width'] == x['height'], images_list))
            rectangular_images = list(filter(lambda x: x['style'] == 'alternate' and x['width'] > x['height'], images_list))
            
            # Select the first image of each type, if available
            if square_images:
                image_urls['square'] = square_images[0]['url']
            if rectangular_images:
                image_urls['rectangular'] = rectangular_images[0]['url']
            
            return image_urls
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_game_image_urls(self, game_name):
        """
        Fetches URLs of square and rectangular images for the game by its name.

        Parameters:
        game_name (str): The name of the game.

        Returns:
        dict: A dictionary containing URLs of square and rectangular images if found, None otherwise.
        """
        game_id = self._fetch_game_id(game_name)
        if game_id:
            return self._fetch_game_urls(game_id)
        else:
            print(f"Could not find game ID for {game_name}")
            return None