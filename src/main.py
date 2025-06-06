#!/usr/bin/env python3

import pygame
import sys
from game import GameManager
from utils import clear_screen

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    """Main entry point for the game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Echoes of the Shardlands - 2D")

    clear_screen()
    game = GameManager()
    # game.run() # This might be blocking, will address later

    running = True
    while running:

        events = pygame.event.get() # Get all events once per frame
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and game.current_game_state == 'playing': # Only allow interaction attempt if playing
                    game.attempt_npc_interaction()
        
        # Handle player input for movement only if game state is 'playing'
        if game.current_game_state == 'playing':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.move_player('left')
            if keys[pygame.K_RIGHT]:
                game.move_player('right')
            if keys[pygame.K_UP]:
                game.move_player('up')
            if keys[pygame.K_DOWN]:
                game.move_player('down')
        
        # Update game logic (like animations)
        game.update_player_animation()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle player input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.move_player('left')
        if keys[pygame.K_RIGHT]:
            game.move_player('right')
        if keys[pygame.K_UP]:
            game.move_player('up')
        if keys[pygame.K_DOWN]:
            game.move_player('down')

            
        # For now, fill the screen with black
        screen.fill((0, 0, 0))
        
        # Draw the current room
        game.draw_current_room(screen)
        
        # Draw the player
        game.draw_player(screen)
        

        # Draw NPCs
        game.draw_npcs(screen)

        # Handle Dialogue UI if in dialogue state
        if game.current_game_state == 'dialogue':
            game.handle_dialogue(screen, events) # Pass events to dialogue handler
        

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        pygame.quit() # Ensure pygame quits on other exceptions too
        raise