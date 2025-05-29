from typing import Dict, List, Optional
from entities import Player, Room, Stats, Item
from world_gen import WorldGenerator
from combat import CombatSystem
from events import EventSystem
from utils import print_colored, get_input, clear_screen, Fore, roll_dice, format_command_help
import os
import json
import random

class GameManager:
    def __init__(self):
        self.world_gen = WorldGenerator()
        self.event_system = EventSystem()
        self.player = self._create_player()
        self.current_room: Optional[Room] = None
        self.all_rooms: List[Room] = []
        self.memory_forge_upgrades = self._initialize_upgrades()
        # Game statistics
        self.stats = {
            'enemies_defeated': 0,
            'rooms_explored': 0,
            'memory_shards_collected': 0,
            'upgrades_purchased': 0,
            'total_damage_dealt': 0,
            'total_damage_taken': 0,
            'play_time': 0,  # In seconds
            'deaths': 0
        }
        
    def _create_player(self) -> Player:
        """Create a new player with starting stats."""
        return Player(
            name="Hero",
            stats=Stats(
                health=80,
                max_health=80,
                attack=10,
                defense=5
            ),
            memory_shards=0
        )
        
    def _initialize_upgrades(self) -> Dict[str, Dict]:
        """Initialize available upgrades in the Memory Forge."""
        return {
            'max_health': {
                'name': 'Increased Vitality',
                'description': 'Increase maximum health by 20',
                'cost': 100,
                'value': 20,
                'purchased': 0,
                'max_purchases': 5,
                'tier': 1
            },
            'attack': {
                'name': 'Enhanced Strike',
                'description': 'Increase attack damage by 5',
                'cost': 150,
                'value': 5,
                'purchased': 0,
                'max_purchases': 3,
                'tier': 1
            },
            'defense': {
                'name': 'Hardened Shell',
                'description': 'Increase defense by 3',
                'cost': 125,
                'value': 3,
                'purchased': 0,
                'max_purchases': 3,
                'tier': 1
            },
            'shard_magnet': {
                'name': 'Shard Magnetism',
                'description': 'Increase Memory Shard gains by 10%',
                'cost': 200,
                'value': 0.1,  # 10% increase
                'purchased': 0,
                'max_purchases': 5,
                'tier': 2,
                'requires': {'max_health': 1, 'attack': 1}  # Requires 1 purchase in each
            },
            'quick_learner': {
                'name': 'Quick Learner',
                'description': 'Gain 1 Memory Shard for each room explored',
                'cost': 300,
                'value': 1,
                'purchased': 0,
                'max_purchases': 1,
                'tier': 2,
                'requires': {'shard_magnet': 1}
            },
            'battle_mastery': {
                'name': 'Battle Mastery',
                'description': 'Gain +1 attack and defense for each enemy defeated in a run',
                'cost': 500,
                'value': 1,
                'purchased': 0,
                'max_purchases': 1,
                'tier': 3,
                'requires': {'attack': 2, 'defense': 2}
            },
            'crystal_affinity': {
                'name': 'Crystal Affinity',
                'description': 'Items have 10% chance to not be consumed on use',
                'cost': 400,
                'value': 0.1,
                'purchased': 0,
                'max_purchases': 3,
                'tier': 2,
                'requires': {'max_health': 2}
            },
            'void_touched': {
                'name': 'Void Touched',
                'description': 'Start each run with a random legendary item',
                'cost': 1000,
                'value': 1,
                'purchased': 0,
                'max_purchases': 1,
                'tier': 3,
                'requires': {'crystal_affinity': 2, 'battle_mastery': 1}
            }
        }
        
    def save_game(self) -> None:
        """Save game progress."""
        save_data = {
            'player': {
                'stats': {
                    'health': self.player.stats.health,
                    'max_health': self.player.stats.max_health,
                    'attack': self.player.stats.attack,
                    'defense': self.player.stats.defense
                },
                'memory_shards': self.player.memory_shards
            },
            'upgrades': self.memory_forge_upgrades
        }
        
        os.makedirs('saves', exist_ok=True)
        with open('saves/save.json', 'w') as f:
            json.dump(save_data, f, indent=2)
            
    def load_game(self) -> bool:
        """Load game progress. Returns True if successful."""
        try:
            with open('saves/save.json', 'r') as f:
                save_data = json.load(f)
                
            player_stats = save_data['player']['stats']
            self.player.stats = Stats(**player_stats)
            self.player.memory_shards = save_data['player']['memory_shards']
            self.memory_forge_upgrades = save_data['upgrades']
            return True
        except FileNotFoundError:
            return False
            
    def calculate_shard_multiplier(self) -> float:
        """Calculate the current Memory Shard gain multiplier."""
        base_multiplier = 1.0
        if 'shard_magnet' in self.memory_forge_upgrades:
            base_multiplier += (
                self.memory_forge_upgrades['shard_magnet']['value'] *
                self.memory_forge_upgrades['shard_magnet']['purchased']
            )
        return base_multiplier
        
    def apply_run_stats(self) -> None:
        """Apply run-based stat bonuses."""
        if 'battle_mastery' in self.memory_forge_upgrades and self.memory_forge_upgrades['battle_mastery']['purchased'] > 0:
            bonus = self.enemies_defeated * self.memory_forge_upgrades['battle_mastery']['value']
            self.player.stats.attack += bonus
            self.player.stats.defense += bonus
            if bonus > 0:
                print_colored(f"\nBattle Mastery: +{bonus} to attack and defense!", Fore.CYAN)
                
    def check_item_preservation(self) -> bool:
        """Check if an item should be preserved after use."""
        if 'crystal_affinity' in self.memory_forge_upgrades:
            preservation_chance = (
                self.memory_forge_upgrades['crystal_affinity']['value'] *
                self.memory_forge_upgrades['crystal_affinity']['purchased']
            )
            return chance(preservation_chance)
        return False
        
    def start_new_run(self) -> None:
        """Start a new run in the Shardlands."""
        # Reset run statistics
        self.enemies_defeated = 0
        self.rooms_explored = 0
        
        # Generate new world
        self.current_room, self.all_rooms = self.world_gen.generate_world()
        
        # Reset player health but keep upgrades
        self.player.stats.health = self.player.stats.max_health
        
        # Apply Void Touched (start with legendary item)
        if ('void_touched' in self.memory_forge_upgrades and 
            self.memory_forge_upgrades['void_touched']['purchased'] > 0):
            legendary_item = self.world_gen.generate_legendary_item()
            if self.player.add_item(legendary_item):
                print_colored(f"\nVoid Touched: Received {legendary_item.name}!", Fore.MAGENTA)
        
        print_colored("\nYou enter the Shardlands...", Fore.CYAN, bold=True)
        
        # Run the game session until death
        while True:
            if not self.handle_room():  # handle_room now returns False on death
                break  # Exit the run loop on death
        
    def handle_room(self) -> bool:
        """Handle player interactions in the current room.
        Returns False if the player died, True otherwise."""
        while True:
            clear_screen()
            
            # Apply run-based stat bonuses
            self.apply_run_stats()
            
            if not self.current_room.visited:
                self.rooms_explored += 1
                # Quick Learner bonus
                if ('quick_learner' in self.memory_forge_upgrades and 
                    self.memory_forge_upgrades['quick_learner']['purchased'] > 0):
                    bonus = self.memory_forge_upgrades['quick_learner']['value']
                    self.player.memory_shards += bonus
                    print_colored(f"Quick Learner: +{bonus} Memory Shards!", Fore.YELLOW)
            
            print_colored(f"\n=== {self.current_room.room_type.upper()} ROOM ===", Fore.CYAN, bold=True)
            print(f"\n{self.current_room.description}")
            print(f"\nYou: {self.player}")
            
            # Show available directions
            available_exits = list(self.current_room.connections.keys())
            if available_exits:
                print("\nAvailable exits:", ', '.join(available_exits))
            else:
                print("\nNo exits available!")
            
            # Handle room based on type
            if not self.current_room.visited:
                if self.current_room.room_type == 'combat' and self.current_room.enemies:
                    combat = CombatSystem(self.player, self.current_room.enemies)
                    survived, loot = combat.run_combat()
                    if not survived:
                        self.handle_death()
                        return False  # Signal player death
                    else:
                        self.enemies_defeated += len(combat.defeated_enemies)
                        # Handle loot
                        if loot:
                            print("\nCollecting loot...")
                            for item in loot:
                                if self.player.can_add_item():
                                    self.player.add_item(item)
                                    print_colored(f"Added {item.name} to inventory!", Fore.GREEN)
                                else:
                                    print_colored("Inventory full! Cannot pick up more items.", Fore.RED)
                                    break
                            input("\nPress Enter to continue...")
                        
                elif self.current_room.room_type == 'treasure' and self.current_room.items:
                    print("\nYou found items!")
                    for item in self.current_room.items:
                        if self.player.can_add_item():
                            self.player.add_item(item)
                            print_colored(f"Added {item.name} to inventory!", Fore.GREEN)
                        else:
                            print_colored("Inventory full! Cannot pick up more items.", Fore.RED)
                            break
                            
                elif self.current_room.room_type == 'event' and self.current_room.event_id:
                    survived = self.event_system.handle_event(self.current_room.event_id, self.player)
                    if not survived:
                        self.handle_death()
                        return False  # Signal player death
                        
                self.current_room.visited = True
            
            # Available commands
            commands = {
                'move': available_exits,
                'inventory': [],
                'status': [],
                'help': []
            }
            
            # Get player action
            action = get_input(
                f"\nWhat would you like to do? ({format_command_help(commands)})",
                valid_options=list(commands.keys()),
                allow_compound=True
            )
            
            # Parse command
            parts = action.split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if command == 'move':
                if not available_exits:
                    print_colored("No exits available!", Fore.RED)
                    continue
                
                if args and args[0] in available_exits:
                    direction = args[0]
                else:
                    direction = get_input(
                        "Choose direction",
                        valid_options=available_exits
                    )
                
                self.current_room = self.current_room.connections[direction]
                return True  # Continue the run in the new room
                
            elif command == 'inventory':
                self.show_inventory()
                
            elif command == 'status':
                self.show_status()
                
            elif command == 'help':
                self.show_help(commands)
                
    def show_inventory(self) -> None:
        """Display and handle inventory."""
        if not self.player.inventory:
            print_colored("\nInventory is empty!", Fore.YELLOW)
            return
            
        print("\nInventory:")
        for i, item in enumerate(self.player.inventory, 1):
            # Color code items based on their target type
            if item.effect_type == 'heal':
                color = Fore.GREEN
                target = "(Self)"
            elif item.effect_type == 'damage':
                color = Fore.RED
                target = "(Enemy)"
            elif item.effect_type in ['attack', 'defense']:
                color = Fore.CYAN
                target = "(Self)"
            else:
                color = Fore.WHITE
                target = ""
                
            print(f"{i}. {color}{item.name} {target}{Fore.WHITE} - {item.description}")
            
        # Available commands for inventory
        commands = {
            'use': [str(i) for i in range(1, len(self.player.inventory) + 1)],
            'back': []
        }
        
        action = get_input(
            f"\nWhat would you like to do? ({format_command_help(commands)})",
            valid_options=list(commands.keys()),
            allow_compound=True
        )
        
        # Parse command and arguments
        parts = action.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if command == 'use':
            if args and args[0] in commands['use']:
                item_idx = int(args[0]) - 1
            else:
                item_idx = int(get_input(
                    "Choose item number",
                    valid_options=[str(i) for i in range(1, len(self.player.inventory) + 1)]
                )) - 1
                
            item = self.player.remove_item(item_idx)
            if item:
                # Check if we're in combat and if the item can target enemies
                in_combat = (self.current_room.room_type == 'combat' and 
                           self.current_room.enemies and 
                           not self.current_room.visited)
                
                if item.effect_type == 'damage':  # Damage items MUST target enemies
                    if not in_combat:
                        self.player.add_item(item)
                        print_colored("Can only use damage items in combat!", Fore.RED)
                        return
                        
                    # Show enemies for targeting
                    print("\nEnemies:")
                    for i, enemy in enumerate(self.current_room.enemies, 1):
                        print(f"{i}. {enemy}")
                        
                    target_idx = int(get_input(
                        "Choose target (number)",
                        valid_options=[str(i) for i in range(1, len(self.current_room.enemies) + 1)]
                    )) - 1
                    target = self.current_room.enemies[target_idx]
                    result = item.use(target)
                    
                    # Check if enemy died
                    if not target.stats.is_alive():
                        print_colored(f"{target.name} was defeated!", Fore.GREEN)
                        self.current_room.enemies.remove(target)
                else:  # Healing and buff items ALWAYS target player
                    result = item.use(self.player)
                        
                print_colored(result, Fore.YELLOW)
                
                # Check for item preservation
                if self.check_item_preservation():
                    self.player.add_item(item)
                    print_colored("Crystal Affinity preserved the item!", Fore.CYAN)
                
    def show_status(self) -> None:
        """Display player status."""
        print(f"\nHealth: {self.player.stats.health}/{self.player.stats.max_health}")
        print(f"Attack: {self.player.stats.attack}")
        print(f"Defense: {self.player.stats.defense}")
        print(f"Memory Shards: {self.player.memory_shards}")
        
    def _handle_easter_egg(self) -> None:
        """Handle the secret '137' input easter egg."""
        clear_screen()
        print_colored("\n=== ANCIENT MEMORY DISCOVERED ===", Fore.MAGENTA, bold=True)
        print("\nAs you focus on the number 137, a mysterious resonance fills your mind...")
        print("\nThe fine-structure constant of the universe whispers its secrets...")
        
        # Give the player a special reward
        special_stats = {
            'health': self.player.stats.health + 37,
            'max_health': self.player.stats.max_health + 37,
            'attack': self.player.stats.attack + 13,
            'defense': self.player.stats.defense + 7
        }
        self.player.stats = Stats(**special_stats)
        self.player.memory_shards += 137
        
        print_colored("\nYou feel your being resonate with cosmic energy!", Fore.CYAN)
        print_colored(f"Health increased by 37!", Fore.GREEN)
        print_colored(f"Attack increased by 13!", Fore.YELLOW)
        print_colored(f"Defense increased by 7!", Fore.BLUE)
        print_colored(f"Gained 137 Memory Shards!", Fore.MAGENTA)
        
        input("\nPress Enter to return to reality...")

    def main_menu(self) -> None:
        """Display and handle the main menu."""
        while True:
            clear_screen()
            print_colored("\n=== ECHOES OF THE SHARDLANDS ===", Fore.CYAN, bold=True)
            print("\n1. New Run")
            print("2. Memory Forge")
            print("3. Quit")
            
            action = get_input(
                "\nChoose action",
                valid_options=['1', '2', '3', '137']  # Secretly accept '137'
            )
            
            if action == '137':
                self._handle_easter_egg()
            elif action == '1':
                self.start_new_run()
            elif action == '2':
                self.memory_forge()
            elif action == '3':
                print_colored("\nThanks for playing!", Fore.YELLOW)
                break
                
    def show_reward(self, shards: int, source: str) -> None:
        """Display a reward notification with fancy formatting."""
        print_colored(f"\n+{shards} Memory Shards from {source}!", Fore.YELLOW, bold=True)
        print_colored(f"Total Memory Shards: {self.player.memory_shards}", Fore.CYAN)
        
    def handle_death(self) -> None:
        """Handle player death."""
        print_colored("\nYou have been defeated!", Fore.RED, bold=True)
        
        # Calculate Memory Shard rewards with bonuses
        rooms_explored = len([r for r in self.all_rooms if r.visited])
        base_shards = rooms_explored * 10
        depth_bonus = max(0, rooms_explored - 5) * 5  # Bonus for exploring deeper
        enemy_bonus = self.enemies_defeated * 5  # Bonus for defeated enemies
        
        total_shards = base_shards + depth_bonus + enemy_bonus
        self.player.memory_shards += total_shards
        
        # Show run summary
        print_colored("\n=== RUN SUMMARY ===", Fore.CYAN, bold=True)
        print("\nYour journey into the Shardlands has ended...")
        print(f"You explored {rooms_explored} rooms and defeated {self.enemies_defeated} enemies")
        
        # Show final stats
        print_colored("\nFinal Stats:", Fore.YELLOW)
        print(f"Health: {self.player.stats.health}/{self.player.stats.max_health}")
        print(f"Attack: {self.player.stats.attack}")
        print(f"Defense: {self.player.stats.defense}")
        
        # Show rewards
        print_colored("\nMemory Shards Earned:", Fore.YELLOW)
        print(f"Base (Exploration): {base_shards}")
        if depth_bonus > 0:
            print(f"Depth Bonus: +{depth_bonus}")
        if enemy_bonus > 0:
            print(f"Combat Bonus: +{enemy_bonus}")
        print_colored(f"\nTotal Shards Earned: {total_shards}", Fore.YELLOW, bold=True)
        
        self.save_game()
        input("\nPress Enter to return to main menu...")
        
    def check_upgrade_requirements(self, upgrade_key: str) -> bool:
        """Check if requirements are met for an upgrade."""
        upgrade = self.memory_forge_upgrades[upgrade_key]
        if 'requires' not in upgrade:
            return True
            
        for req_key, req_amount in upgrade['requires'].items():
            if self.memory_forge_upgrades[req_key]['purchased'] < req_amount:
                return False
        return True

    def memory_forge(self) -> None:
        """Handle the Memory Forge upgrade system."""
        while True:
            clear_screen()
            print_colored("\n=== MEMORY FORGE ===", Fore.CYAN, bold=True)
            print(f"\nMemory Shards: {self.player.memory_shards}")
            
            # Group upgrades by tier
            upgrades_by_tier: Dict[int, List[str]] = {}
            for key, upgrade in self.memory_forge_upgrades.items():
                if upgrade['purchased'] < upgrade['max_purchases']:
                    tier = upgrade.get('tier', 1)
                    if tier not in upgrades_by_tier:
                        upgrades_by_tier[tier] = []
                    upgrades_by_tier[tier].append(key)
            
            if not upgrades_by_tier:
                print_colored("\nAll upgrades maxed out!", Fore.YELLOW)
                break
            
            # Display upgrades by tier
            available_upgrades = []
            for tier in sorted(upgrades_by_tier.keys()):
                print_colored(f"\nTier {tier} Upgrades:", Fore.YELLOW, bold=True)
                for key in upgrades_by_tier[tier]:
                    upgrade = self.memory_forge_upgrades[key]
                    meets_requirements = self.check_upgrade_requirements(key)
                    
                    if meets_requirements:
                        available_upgrades.append(key)
                        print(f"{len(available_upgrades)}. {upgrade['name']} "
                              f"({upgrade['description']}) - Cost: {upgrade['cost']} "
                              f"[{upgrade['purchased']}/{upgrade['max_purchases']}]")
                    else:
                        print_colored(f"? {upgrade['name']} - Requires: ", Fore.RED, end='')
                        reqs = []
                        for req_key, req_amount in upgrade['requires'].items():
                            req_name = self.memory_forge_upgrades[req_key]['name']
                            current = self.memory_forge_upgrades[req_key]['purchased']
                            reqs.append(f"{req_name} ({current}/{req_amount})")
                        print_colored(', '.join(reqs), Fore.RED)
            
            actions = ['back'] + [str(i) for i in range(1, len(available_upgrades) + 1)]
            action = get_input(
                "\nChoose upgrade to purchase (number or 'back')",
                valid_options=actions
            )
            
            if action == 'back':
                break
                
            upgrade_key = available_upgrades[int(action) - 1]
            upgrade = self.memory_forge_upgrades[upgrade_key]
            
            if self.player.memory_shards >= upgrade['cost']:
                self.player.memory_shards -= upgrade['cost']
                upgrade['purchased'] += 1
                
                # Apply upgrade
                if upgrade_key == 'max_health':
                    self.player.stats.max_health += upgrade['value']
                    self.player.stats.health = self.player.stats.max_health
                elif upgrade_key == 'attack':
                    self.player.stats.attack += upgrade['value']
                elif upgrade_key == 'defense':
                    self.player.stats.defense += upgrade['value']
                elif upgrade_key == 'shard_magnet':
                    # This will be applied in reward calculations
                    pass
                elif upgrade_key == 'quick_learner':
                    # This will be applied in room exploration
                    pass
                elif upgrade_key == 'battle_mastery':
                    # This will be applied in combat
                    pass
                elif upgrade_key == 'crystal_affinity':
                    # This will be applied in item usage
                    pass
                elif upgrade_key == 'void_touched':
                    # This will be applied at run start
                    pass
                    
                print_colored(f"\nPurchased {upgrade['name']}!", Fore.GREEN)
                self.save_game()
            else:
                print_colored("\nNot enough Memory Shards!", Fore.RED)
                
    def run(self) -> None:
        """Start the game."""
        # Try to load saved game
        if not self.load_game():
            print_colored("Starting new game...", Fore.YELLOW)
            self.save_game()
            
        self.main_menu()

    def calculate_difficulty_tier(self) -> int:
        """Calculate current difficulty tier based on total upgrades purchased."""
        total_upgrades = sum(upgrade['purchased'] for upgrade in self.memory_forge_upgrades.values())
        return max(1, total_upgrades // 3)  # Every 3 upgrades increases difficulty tier

    def show_help(self, commands: Dict[str, List[str]]) -> None:
        """Show help text for available commands."""
        print_colored("\nAvailable Commands:", Fore.CYAN, bold=True)
        print("  move [direction] - Move to another room")
        print("  inventory       - View and use items")
        print("  status         - View player status")
        print("  help           - Show this help text")
        print("\nTip: You can combine commands with arguments (e.g., 'move north')")
        input("\nPress Enter to continue...")