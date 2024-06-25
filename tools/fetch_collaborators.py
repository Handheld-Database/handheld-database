import requests
import json
import os

# Load the GitHub token from the environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise EnvironmentError("GITHUB_TOKEN environment variable not set")

# Replace these with your repository details
owner = "ogregorio"
repo = "handheld-database"

# GitHub API URL for fetching collaborators
url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"

# Headers with the personal access token for authentication
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch the list of collaborators
response = requests.get(url, headers=headers)

if response.status_code == 200:
    collaborators = response.json()
    
    # Extract required attributes from each collaborator
    collaborators_data = [
        {
            "login": collaborator["login"],
            "avatar_url": collaborator["avatar_url"]
        }
        for collaborator in collaborators
    ]

    # Ensure the directory exists
    os.makedirs("commons/collaborators", exist_ok=True)
    
    # Write the list to a JSON file
    with open("commons/collaborators/collaborators.json", "w") as json_file:
        json.dump(collaborators_data, json_file, indent=4)

    print("Collaborators have been written to commons/collaborators/collaborators.json")
else:
    print(f"Failed to fetch collaborators: {response.status_code} - {response.text}")