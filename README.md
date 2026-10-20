# Aditya Mukherjee — Interactive Pixel-Art Portfolio

An interactive portfolio built with **React, Vite, and Phaser 3**. Explore a pixel-art room and interact with objects to discover my projects, technical skills, background, and contact information.

## Live Demo

**Explore the portfolio:** [Aditya Mukherjee — Interactive Portfolio](YOUR_DEPLOYED_LINK_HERE)

Explore the pixel-art room, interact with objects, and discover my projects, tech stack, background, and contact details.

## Features

- Interactive pixel-art room with keyboard movement.
- Clickable objects and proximity-based interactions.
- Contextual dialogue and portfolio panels.
- Custom player character and room textures.
- Persistent controls hint, separate from the dialogue box.
- Game-style navigation instead of a conventional portfolio layout.

## Controls

| Action | Control |
|---|---|
| Move | Arrow keys (`↑` `↓` `←` `→`) |
| Inspect the nearest object | `E` |
| Inspect an object directly | Click the object |
| Dismiss dialogue | **Cancel** or the available close control |

**Movement uses the arrow keys only. WASD is not supported.**

Walk close to an interactive object and press `E`, or click it to inspect it.

## Explore the Room

| Object | Portfolio section |
|---|---|
| PC / workstation | Projects |
| Bed | About Me |
| Bookshelf and notes | Tech Stack |
| TV | Contact Details |

## Tech Stack

- **React** — interface, dialogue, overlays, and portfolio panels.
- **Vite** — development server and production bundling.
- **Phaser 3** — game scene, player movement, room rendering, and interactions.
- **JavaScript** — application and game logic.
- **CSS** — layout, HUD, dialogue, and panel styling.
- **Pixel-art assets** — character, furniture, and room decorations.

## Architecture

The application separates the game world from the portfolio interface.

```text
React Application
├── App.jsx
│   ├── Tracks the active portfolio section
│   └── Renders the HUD, dialogue, and content panels
├── game/
│   ├── GameCanvas.jsx
│   │   └── Creates and mounts the Phaser game
│   └── RoomScene.js
│       ├── Builds the room and furniture
│       ├── Creates the player and handles movement
│       ├── Defines interactive objects
│       └── Sends interaction events to React
├── data/
│   └── portfolio.js
│       └── Stores projects, skills, education, and contact data
└── styles.css
    └── Styles the game layout, HUD, dialogue, and panels
```

*This describes the intended separation of responsibilities; adjust the tree if your current source files differ.*

### Interaction Flow

1. Phaser renders the room and handles player movement.
2. The player approaches an object and presses `E`, or clicks it.
3. The Phaser scene reports the selected object to React through callbacks.
4. React displays the relevant portfolio section.
5. The controls hint stays visible independently of the contextual dialogue.

## Getting Started

### Prerequisites

- Node.js — a current LTS release is recommended.
- npm.

### Installation

Open a terminal in the project directory and run:

```bash
npm install
```

### Development

```bash
npm run dev
```

Open the local URL printed by Vite.

### Production Build

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## Customization

### Portfolio Content

Edit the portfolio data file, such as `src/data/portfolio.js`, to update project descriptions, skills, education, and contact details. Verify personal links before publishing.

### Room and Interactions

The Phaser scene, such as `src/game/RoomScene.js`, controls room layout, object positions, interaction zones, player spawn position, and movement. When moving an object, update its interaction zone as well.

### Interface

React components and the stylesheet control the persistent controls hint, dialogue box, character portrait, and portfolio panels. Keep the controls hint separate from the dialogue so instructions remain visible while the dialogue is closed.

### Textures

Ensure texture paths and keys match those used by Phaser's loading code. Use pixel-art rendering settings and avoid uneven sprite scaling to preserve crisp edges.

## Featured Projects

- **AdiFlash** — multimodal flashcard generator built with Flask, Gemini, and SQLite.
- **FolkSocial** — social microplatform built with Flask and SQLite.
- **NetSentient** — semantic network router; Top 10 at IEEE Computer Society HackBattle during graVITas.
- **FolkNotes** — MERN notes application featuring search, favorites, themes, and rate limiting.

## Deployment

Run `npm run build` and deploy the generated `dist/` directory to a static host that supports Vite applications. If deploying under a subpath, configure Vite's `base` option accordingly.

## Troubleshooting

- **The game won't start:** Run `npm install` and inspect the terminal for missing dependencies or import errors.
- **Textures are missing:** Verify the texture paths and keys in the Phaser loading code.
- **An object is difficult to interact with:** Check that its interaction area matches its visible position and size.
- **The room looks stretched:** Check Phaser's scale configuration and the CSS dimensions of the game container.
- **The HUD overlaps the dialogue:** Keep them as separate UI elements and account for both when setting their positions.

## Credits

Created by **Aditya Mukherjee**.

Built with React, Vite, Phaser 3, JavaScript, and pixel-art assets.