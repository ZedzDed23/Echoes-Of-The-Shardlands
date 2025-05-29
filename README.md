# Echoes of the Shardlands

A text-based incremental roguelite game where you explore procedurally generated Shardlands, collect Memory Shards, and progress through permanent upgrades.

## Features

- Procedurally generated environments
- Turn-based combat system
- Permadeath with persistent progression
- Memory Shard upgrade system
- Diverse enemy types
- Random events with meaningful choices
- Item collection and management

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python src/main.py
```

## Game Controls

- Use number keys to select options from menus
- Follow on-screen prompts for navigation and actions
- Type 'quit' at any time to exit the game

## Development

The game is structured into several key components:
- Procedural generation system
- Combat system
- Progression system
- Event system
- Inventory system

To run tests:
```bash
pytest tests/
```

## License

MIT License - See LICENSE file for details 