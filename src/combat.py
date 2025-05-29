from typing import List, Optional, Tuple
from entities import Player, Enemy, Item
from utils import print_colored, get_input, roll_dice, Fore, chance, format_command_help

class CombatSystem:
    def __init__(self, player: Player, enemies: List[Enemy]):
        self.player = player
        self.enemies = enemies
        self.turn_count = 0
        self.defeated_enemies: List[Enemy] = []  # Track defeated enemies for loot
        
    def generate_loot_item(self, item_name: str, enemy_level: int) -> Item:
        """Generate a loot item based on the item name and enemy level."""
        # Determine rarity based on enemy level and chance
        rarity_roll = roll_dice(1, 100)
        if rarity_roll <= 5:  # 5% chance for legendary
            rarity = 'legendary'
            multiplier = 3.0
        elif rarity_roll <= 15:  # 10% chance for rare
            rarity = 'rare'
            multiplier = 2.0
        elif rarity_roll <= 35:  # 20% chance for uncommon
            rarity = 'uncommon'
            multiplier = 1.5
        else:  # 65% chance for common
            rarity = 'common'
            multiplier = 1.0
            
        # Scale value based on enemy level
        base_value = {
            'health_potion': 20,
            'damage_crystal': 15,
            'shield_shard': 5,
            'power_fragment': 3
        }.get(item_name, 10)
        
        value = int(base_value * multiplier * (1 + enemy_level * 0.2))
        
        # Special legendary variations
        if rarity == 'legendary':
            if item_name == 'health_potion':
                name = "Phoenix Elixir"
                description = "A legendary potion that provides massive healing"
            elif item_name == 'damage_crystal':
                name = "Void Shard"
                description = "A crystal infused with void energy"
            else:
                name = f"Legendary {item_name.replace('_', ' ').title()}"
                description = f"A legendary item of immense power"
        else:
            name = f"{rarity.capitalize()} {item_name.replace('_', ' ').title()}"
            description = f"A {rarity} item that provides {value} {item_name.split('_')[0]}"
            
        return Item(
            name=name,
            description=description,
            effect_type=item_name.split('_')[0],
            effect_value=value,
            rarity=rarity,
            durability=roll_dice(3, 5) if chance(0.3) else None
        )
        
    def player_turn(self) -> bool:
        """Handle player's turn. Returns True if player flees."""
        print_colored("\nYour turn!", Fore.CYAN, bold=True)
        print(f"\nYou: {self.player}")
        print("\nEnemies:")
        for i, enemy in enumerate(self.enemies, 1):
            print(f"{i}. {enemy}")
            
        # Get action choice with available targets for compound commands
        actions = {
            'attack': [str(i) for i in range(1, len(self.enemies) + 1)],
            'item': [str(i) for i in range(1, len(self.player.inventory) + 1)] if self.player.inventory else [],
            'flee': []
        }
        
        action = get_input(
            f"\nWhat would you like to do? ({format_command_help(actions)})",
            valid_options=list(actions.keys()),
            allow_compound=True
        )
        
        # Parse command and arguments
        parts = action.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if command == 'attack':
            if len(self.enemies) == 1:
                target = self.enemies[0]
            else:
                if args and args[0] in actions['attack']:
                    target_idx = int(args[0]) - 1
                else:
                    target_idx = int(get_input(
                        "Choose target (number)",
                        valid_options=[str(i) for i in range(1, len(self.enemies) + 1)]
                    )) - 1
                target = self.enemies[target_idx]
            
            # Calculate and deal damage
            base_damage = self.player.stats.attack
            damage = roll_dice(base_damage - 2, base_damage + 2)
            actual_damage = target.stats.take_damage(damage)
            
            print_colored(
                f"\nYou attack {target.name} for {actual_damage} damage!",
                Fore.YELLOW
            )
            
            # Check if enemy died
            if not target.stats.is_alive():
                print_colored(f"{target.name} was defeated!", Fore.GREEN)
                self.defeated_enemies.append(target)
                self.enemies.remove(target)
                
        elif command == 'item':
            if not self.player.inventory:
                print_colored("You have no items!", Fore.RED)
                return self.player_turn()  # Try again
                
            print("\nInventory:")
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item.name} - {item.description}")
                
            if args and args[0] in actions['item']:
                item_idx = int(args[0])
            else:
                item_idx = int(get_input(
                    "Choose item to use (number, or 0 to cancel)",
                    valid_options=['0'] + [str(i) for i in range(1, len(self.player.inventory) + 1)]
                ))
            
            if item_idx == 0:
                return self.player_turn()  # Try again
                
            item = self.player.remove_item(item_idx - 1)
            if item:
                if item.effect_type in ['heal', 'buff']:
                    result = item.use(self.player)
                else:
                    if len(self.enemies) == 1:
                        target = self.enemies[0]
                    else:
                        # Check for additional target argument
                        if len(args) > 1 and args[1] in [str(i) for i in range(1, len(self.enemies) + 1)]:
                            target_idx = int(args[1]) - 1
                        else:
                            target_idx = int(get_input(
                                "Choose target (number)",
                                valid_options=[str(i) for i in range(1, len(self.enemies) + 1)]
                            )) - 1
                        target = self.enemies[target_idx]
                    result = item.use(target)
                    
                    if not target.stats.is_alive():
                        print_colored(f"{target.name} was defeated!", Fore.GREEN)
                        self.defeated_enemies.append(target)
                        self.enemies.remove(target)
                        
                print_colored(result, Fore.YELLOW)
                
        elif command == 'flee':
            if roll_dice(1, 100) <= 40:  # 40% chance to flee
                print_colored("You successfully fled from combat!", Fore.GREEN)
                return True
            print_colored("Failed to flee!", Fore.RED)
            
        return False
        
    def enemy_turn(self) -> None:
        """Handle enemies' turns."""
        for enemy in self.enemies:
            print(f"\n{enemy.name}'s turn!")
            
            action = enemy.get_next_action()
            if action == 'attack':
                # Calculate and deal damage
                base_damage = enemy.stats.attack
                damage = roll_dice(base_damage - 1, base_damage + 1)
                actual_damage = self.player.stats.take_damage(damage)
                
                print_colored(
                    f"{enemy.name} attacks you for {actual_damage} damage!",
                    Fore.RED
                )
                
    def run_combat(self) -> Tuple[bool, List[Item]]:
        """Run the complete combat sequence. Returns (player_survived, loot)."""
        print_colored("\nCombat started!", Fore.RED, bold=True)
        self.defeated_enemies = []  # Reset defeated enemies list
        
        while True:
            # Player turn
            fled = self.player_turn()
            if fled:
                return True, []  # Player survived but gets no loot
                
            # Check if all enemies defeated
            if not self.enemies:
                print_colored("\nVictory!", Fore.GREEN, bold=True)
                
                # Generate loot from all defeated enemies
                loot = []
                for enemy in self.defeated_enemies:
                    # Guaranteed drop based on enemy level
                    loot.append(self.generate_loot_item('health_potion', enemy.level))
                    
                    # Random drops from loot table
                    for item_name, drop_chance in enemy.loot_table.items():
                        if chance(drop_chance):
                            loot.append(self.generate_loot_item(item_name, enemy.level))
                            
                if loot:
                    print_colored("\nLoot dropped:", Fore.YELLOW)
                    for item in loot:
                        color = {
                            'legendary': Fore.MAGENTA,
                            'rare': Fore.RED,
                            'uncommon': Fore.GREEN,
                            'common': Fore.WHITE
                        }[item.rarity]
                        print_colored(f"- {item.name}: {item.description}", color)
                        
                return True, loot
                
            # Check if player died
            if not self.player.stats.is_alive():
                print_colored("\nYou have been defeated!", Fore.RED, bold=True)
                return False, []
                
            # Enemy turns
            self.enemy_turn()
            
            # Check if player died after enemy turns
            if not self.player.stats.is_alive():
                print_colored("\nYou have been defeated!", Fore.RED, bold=True)
                return False, []
                
            self.turn_count += 1 