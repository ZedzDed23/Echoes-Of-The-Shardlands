import os
import json
import random
from typing import Any, Dict, List, Optional
from colorama import Fore, Style, init

# Initialize colorama
init()

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json_data(filepath: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json_data(filepath: str, data: Dict[str, Any]) -> None:
    """Save data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def print_colored(text: str, color: str = Fore.WHITE, bold: bool = False, end: str = '\n') -> None:
    """Print colored text."""
    style = Style.BRIGHT if bold else ""
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def get_input(prompt: str, valid_options: Optional[List[str]] = None, allow_compound: bool = False) -> str:
    """Get user input with validation.
    
    Args:
        prompt: The prompt to display to the user
        valid_options: List of valid input options
        allow_compound: If True, allows space-separated compound commands
    """
    while True:
        user_input = input(f"{prompt}: ").strip().lower()
        
        if user_input == 'quit':
            raise SystemExit("Thanks for playing!")
        
        if not valid_options:
            return user_input
            
        if allow_compound:
            # Split input into parts (e.g., "move east" -> ["move", "east"])
            parts = user_input.split()
            if not parts:
                continue
                
            # Check if the first word is a valid command
            command = parts[0]
            if command not in valid_options:
                print_colored(f"Invalid command. Please choose from: {', '.join(valid_options)}", Fore.RED)
                continue
                
            return user_input
        else:
            if user_input in valid_options:
                return user_input
                
            print_colored(f"Invalid input. Please choose from: {', '.join(valid_options)}", Fore.RED)

def roll_dice(min_val: int, max_val: int) -> int:
    """Generate a random number between min_val and max_val."""
    return random.randint(min_val, max_val)

def chance(probability: float) -> bool:
    """Return True with the given probability (0-1)."""
    return random.random() < probability

def format_health(current: int, maximum: int) -> str:
    """Format health display with colors."""
    health_percent = current / maximum
    if health_percent > 0.7:
        color = Fore.GREEN
    elif health_percent > 0.3:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    return f"{color}{current}/{maximum}{Style.RESET_ALL}"

def format_stat_change(value: int, is_positive: bool = True) -> str:
    """Format a stat change with color and sign."""
    color = Fore.GREEN if is_positive else Fore.RED
    sign = '+' if is_positive else ''
    return f"{color}{sign}{value}{Style.RESET_ALL}"

def format_command_help(commands: Dict[str, List[str]]) -> str:
    """Format command help text with available subcommands.
    
    Args:
        commands: Dictionary of commands and their subcommands
    """
    help_text = []
    for cmd, subcmds in commands.items():
        if subcmds:
            help_text.append(f"{cmd} [{'/'.join(subcmds)}]")
        else:
            help_text.append(cmd)
    return ', '.join(help_text) 