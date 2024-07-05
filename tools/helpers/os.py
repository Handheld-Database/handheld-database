# Function to get user input and strip leading/trailing whitespace
def scan_input(prompt):
    """
    Prompts the user for input and returns the input string with leading and trailing whitespace removed.

    Parameters:
    prompt (str): The prompt message displayed to the user.

    Returns:
    str: The user's input with leading and trailing whitespace removed.
    """
    return input(prompt).strip()

# Function to get array input from user, split by ';', and strip whitespace
def scan_array_input(prompt):
    """
    Prompts the user for input, splits the input string by ';' into an array, and strips leading and trailing whitespace from each element.

    Parameters:
    prompt (str): The prompt message displayed to the user.

    Returns:
    list: A list of strings obtained by splitting the user's input by ';' and stripping whitespace from each element.
    """
    return input(prompt).strip().split(';')