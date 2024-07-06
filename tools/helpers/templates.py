def generate_game_templates_md(game_name, normalize_system_name):
    templates = {
        "default": (
            "## {game_name}\n\n%game_overview%\n\n# Execution information\n"
            "**Tester**:\n"
        ),
        "saturn": (
            "## {game_name}\n\n%game_overview%\n\n# Execution information\n"
            "**Tester**:\n\n**SH2 Core**:\n\n**Polygon Mode**:\n\n**Auto-frameskip**:\n\n**Resolution Mode**:\n\n**RGB Resolution Mode**:\n\n**RGB use compute shader for RGB**:"
        ),
        "ports": (
            "## {game_name}\n\n%game_overview%\n\n# Installation\n"
            "**Tester**:\nGive instructions about the installation on the OS you used.\n\n"
            "# Troubleshoot\nDelete this if not needed."
        )
    }

    # Choose the template based on the system name
    template_key = 'ports' if normalize_system_name == 'ports' else 'default'
    template = templates.get(template_key, templates['default'])

    # Format the template with the game name
    game_md_content = template.format(game_name=game_name)

    return game_md_content