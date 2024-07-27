import re
# Function to normalize input string by removing extra spaces and non-word characters
def normalize_string(input_string):
    """
    Normalizes an input string by removing extra spaces and non-word characters.

    Parameters:
    input_string (str): The string to be normalized.

    Returns:
    str: The normalized string.
    """
    # Collapse multiple spaces into one
    normalized_string = re.sub(r'\s+', ' ', input_string)
    # Remove non-word characters
    normalized_string = re.sub(r'[^\w\s]', '', normalized_string)
    # Remove leading/trailing spaces
    normalized_string = normalized_string.strip()
    return normalized_string
# Function to normalize input string by removing all spaces, non-word characters and converting to lower case
def normalize_string_lower(input_string):
    """
    Normalizes an input string by removing all spaces, non-word characters, 
    and converting the string to lower case.

    Parameters:
    input_string (str): The string to be normalized.

    Returns:
    str: The normalized string.
    """
    # Use the normalize_string function to remove extra spaces and non-word characters
    normalized_string = normalize_string(input_string)
    # Convert the string to lower case
    normalized_string = normalized_string.lower()
    # Remove all spaces
    normalized_string = re.sub(r'\s+', '', normalized_string)
    return normalized_string

def extract_game_name(filename):
    """
    Extracts the clean game name from the filename by removing the file extension,
    region codes, [!], and other parenthetical content.

    Parameters:
    filename (str): The filename to extract the game name from.

    Returns:
    str: The extracted game name.
    """
    # Remove file extension
    filename = re.sub(r'\.zip$', '', filename)
    # Remove region codes, [!], and other parenthetical content
    filename = re.sub(r'\s*\(.*?\)\s*', '', filename)
    filename = re.sub(r'\s*\[!\]\s*', '', filename)
    return filename.strip()
