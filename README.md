# Contributing to the Handheld Database

## Introduction
Thank you for considering contributing to our games compatibility list project. This document provides guidelines on how to add new games, platforms, and systems, ensuring our repository remains organized and easy to navigate.

## How to Contribute

### Adding a New Game
1. **Create Game Images:**
    - Add the game's cover image to `commons/images/games/` with the format `[gamename].cover.webp`.
    - Add the game's icon image to `commons/images/games/` with the format `[gamename].icon.webp`.

2. **Create Game Overview:**
    - Add a Markdown file with general game information to `commons/overviews/`. Follow the naming convention `[gamename].md`.

2. **Create Game Data:**
    - Navigate to the appropriate platform and system directory under `platforms/`.
    - Create a new directory for the game if it doesn't already exist. For example, `platforms/tsp/systems/ports/[gamename]/`.
    - Add a JSON file with the game's data. Follow the naming convention `[gamename].json`.
    - Add a Markdown file with specif plarform game instructions. Follow the naming convention `[gamename].md`.
    - Use %game_overview% to indicate where the overview file should be rendered inside `[gamename].md`.

### Adding a New Platform
1. **Create Platform Images:**
    - Add the platform's image to `commons/images/platforms/` with the format `[platformname].webp`.

2. **Create Platform Data:**
    - Navigate to the `platforms/` directory.
    - Create a new directory for the platform if it doesn't already exist.
    - Add an `index.json` file with the platform's data.

### Adding a New System
1. **Create System Images:**
    - Add the system's image to `commons/images/systems/` with the format `[systemname].webp`.

2. **Create System Data:**
    - Navigate to the appropriate platform directory under `platforms/`.
    - Create a new directory for the system if it doesn't already exist. For example, `platforms/[platformname]/systems/[systemname]/`.
    - Add an `index.json` file with the system's data.

## Adding a New Game Automation

This script helps you manage platforms, systems, and games by creating and updating corresponding JSON and Markdown files.

## Prerequisites

- Python 3.x
- JSON module
- OS module
- SYS module
- RE module

## Usage

Run the script with the appropriate command to create platforms, systems, and games.

### Commands

- `new platform [platform_name]`: Create a new platform.
- `new system [platform_name] [system_name]`: Create a new system under a specified platform.
- `new game [platform_name] [system_name] [game_name]`: Create a new game under a specified platform and system.
- `help`: Display the help message.

### Examples

- Create a new platform:

  ```bash
  python tools/new_file.py new platform myplatform

## Commit Guidelines
- Write clear, concise commit messages.
- Include a detailed description of your changes in the commit body.

## Pull Request Process
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

## Media

1. **Usage of WebP Format for Web Application:**

When integrating images into your web application, ensure to utilize the WebP format for optimal performance. WebP offers efficient compression and supports transparency, making it ideal for a variety of graphical elements.

2. **Icon Specifications:**

Icons should be provided in the dimensions of 512x512 pixels to ensure clarity and compatibility across different display resolutions.

3. **Banner Requirements:**

Banners should be provided in the dimensions of 1050x380 pixels to ensure clarity and compatibility across different display resolutions.