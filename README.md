# Contributing to the Handheld Database

## Introduction

Thank you for considering contributing to our games compatibility list project. This document provides guidelines on how to add new games, platforms, and systems, ensuring our repository remains organized and easy to navigate.

## How to Contribute

### Adding a New Game

1. **Create a Review File:**
    - Create a Markdown file for the game review in the format: `gamekey.username.md`.

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

## Game Indexing and Ranking

- **Game Indexing:** Games are now indexed automatically. There's no need for manual creation of game directories or JSON files.
- **Rank Generation:** The game ranking is generated automatically based on the review file.

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

## Rank

### PLATINUM
- **Graphics:** Outstanding, with no glitches or visual issues and exceptional detail.
- **Gameplay:** Extremely stable, with very high FPS (60 or higher) and absolutely no drops or stuttering.
- **Load:** Instantaneous loading, completely free of crashes or any issues affecting user experience.

### GOLD
- **Graphics:** Excellent, without significant glitches or visual issues.
- **Gameplay:** Very stable, with a high FPS rate (30 or higher) and no noticeable drops or stuttering.
- **Load:** Quick loading, no crashes, or issues that affect the user experience.

### SILVER
- **Graphics:** Good, with some minor glitches that do not significantly affect the gaming experience.
- **Gameplay:** Stable most of the time, with occasional minor FPS drops or stuttering.
- **Load:** Relatively quick loading, with few slowdowns or minor issues that can be worked around.

### BRONZE
- **Graphics:** Acceptable, but with noticeable visual glitches that can affect the gaming experience.
- **Gameplay:** Inconsistent, with more frequent and noticeable FPS drops and occasional stuttering.
- **Load:** Slow loading, with the possibility of crashes or issues that affect usability.

### FAULTY
- **Graphics:** Poor, with severe glitches and visual issues that hinder gameplay.
- **Gameplay:** Very unstable, with constant FPS drops and severe stuttering, compromising playability.
- **Load:** Significant loading problems, including frequent crashes and glitches that impede proper use.
