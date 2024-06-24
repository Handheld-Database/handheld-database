# Contributing to the Gameheld Database

## Introduction
Thank you for considering contributing to our games compatibility list project. This document provides guidelines on how to add new games, platforms, and systems, ensuring our repository remains organized and easy to navigate.

## How to Contribute

### Adding a New Game
1. **Create Game Images:**
    - Add the game's cover image to `commons/images/games/` with the format `[gamename].cover.webp`.
    - Add the game's icon image to `commons/images/games/` with the format `[gamename].icon.webp`.

2. **Create Game Data:**
    - Navigate to the appropriate platform and system directory under `platforms/`.
    - Create a new directory for the game if it doesn't already exist. For example, `platforms/tsp/systems/ports/[gamename]/`.
    - Add a JSON file with the game's data. Follow the naming convention `[gamename].json`.
    - Add a Markdown file with additional game information. Follow the naming convention `[gamename].md`.

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