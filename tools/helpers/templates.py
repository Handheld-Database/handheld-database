def generate_game_templates_md(game_name, normalized_system_name):
    templates = {
        "default": (
            "# Execution information\n\n"
            "**Tester**:\n\n**Rank**:\n\n"
        ),
        "saturn": (
            "**Tester**:\n\n**Rank**:\n\n"
            "# Execution information\n\n"
            "**SH2 Core**:\n\n**Polygon Mode**:\n\n**Auto-frameskip**:\n\n**Resolution Mode**:\n\n**RGB Resolution Mode**:\n\n**RGB use compute shader for RGB**:"
        ),
        "ports": (
            "**Tester**:\n\n**Rank**:\n\n"
            "# Installation\n\n"
            "Give instructions about the installation on the OS you used.\n\n"
            "# Troubleshoot\nDelete this if not needed."
        ),
        "psp": (
            "**Tester**:\n\n**Rank**:\n\n"
            "# Execution information\n\n"
            "**Backend**:\n**Resolution**:\n**Frameskip**:\n**Autoframeskip**:\n**Note**:"
        ),
        "nds": (
            "**Tester**:\n\n**Rank**:\n\n"
            "# Execution information\n\n"
            "**High-Resolution 3D**:\n**Frame Skip Type**:\n**Frame Skip Value**:\n**Note**:"
        )
    }

    #print("normalized_system_name", normalized_system_name)
    # Choose the template based on the system name
    template = templates.get(normalized_system_name, templates['default'])

    # Format the template with the game name
    game_md_content = template.format(game_name=game_name)

    return game_md_content