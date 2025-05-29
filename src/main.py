#!/usr/bin/env python3

from game import GameManager
from utils import clear_screen

def main():
    """Main entry point for the game."""
    clear_screen()
    game = GameManager()
    game.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        raise 