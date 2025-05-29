from dataclasses import dataclass, field
from typing import Dict, List, Optional
from utils import format_health, roll_dice

@dataclass
class Stats:
    health: int
    max_health: int
    attack: int
    defense: int
    
    def is_alive(self) -> bool:
        return self.health > 0
        
    def take_damage(self, amount: int) -> int:
        """Apply damage and return actual damage dealt."""
        mitigated = max(0, amount - self.defense)
        self.health = max(0, self.health - mitigated)
        return mitigated
        
    def heal(self, amount: int) -> int:
        """Heal and return amount healed."""
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

@dataclass
class Entity:
    name: str
    stats: Stats
    level: int = 1
    
    def __str__(self) -> str:
        return f"{self.name} [HP: {format_health(self.stats.health, self.stats.max_health)}]"

@dataclass
class Item:
    name: str
    description: str
    effect_type: str  # 'heal', 'damage', 'buff', etc.
    effect_value: int
    rarity: str  # 'common', 'uncommon', 'rare', 'legendary'
    durability: Optional[int] = None
    special_effect: Optional[str] = None  # For legendary items
    
    def use(self, target: 'Entity') -> str:
        """Use item on target and return result message."""
        if self.effect_type == 'heal':
            amount = target.stats.heal(self.effect_value)
            return f"{target.name} healed for {amount} HP"
            
        elif self.effect_type == 'damage':
            amount = target.stats.take_damage(self.effect_value)
            return f"{target.name} took {amount} damage"
            
        elif self.effect_type == 'attack':
            # Temporary attack buff
            target.stats.attack += self.effect_value
            return f"{target.name} gained {self.effect_value} attack power"
            
        elif self.effect_type == 'defense':
            # Temporary defense buff
            target.stats.defense += self.effect_value
            return f"{target.name} gained {self.effect_value} defense"
            
        return "Item had no effect"
    
    def can_target_self(self) -> bool:
        """Whether this item can be used on the player."""
        return self.effect_type in ['heal', 'attack', 'defense']
    
    def can_target_enemy(self) -> bool:
        """Whether this item can be used on enemies."""
        return self.effect_type in ['damage']

@dataclass
class Player(Entity):
    memory_shards: int = 0
    inventory: List[Item] = field(default_factory=list)
    max_inventory: int = 10
    
    def can_add_item(self) -> bool:
        return len(self.inventory) < self.max_inventory
        
    def add_item(self, item: Item) -> bool:
        if not self.can_add_item():
            return False
        self.inventory.append(item)
        return True
        
    def remove_item(self, index: int) -> Optional[Item]:
        if 0 <= index < len(self.inventory):
            return self.inventory.pop(index)
        return None

@dataclass
class Enemy(Entity):
    attack_pattern: List[str] = field(default_factory=list)
    loot_table: Dict[str, float] = field(default_factory=dict)  # item_name: drop_chance
    experience_value: int = 0
    
    def get_next_action(self) -> str:
        """Get the next action from the attack pattern."""
        if not self.attack_pattern:
            return 'attack'  # Default action
        return self.attack_pattern[0]  # In a real implementation, we'd rotate the pattern

@dataclass
class Room:
    room_type: str  # 'combat', 'treasure', 'event'
    description: str
    enemies: List[Enemy] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    event_id: Optional[str] = None
    visited: bool = False
    connections: Dict[str, 'Room'] = field(default_factory=dict)  # direction: room
    
    def add_connection(self, direction: str, room: 'Room') -> None:
        self.connections[direction] = room
        # Add reverse connection
        reverse_dir = {'north': 'south', 'south': 'north', 
                      'east': 'west', 'west': 'east'}
        if direction in reverse_dir:
            room.connections[reverse_dir[direction]] = self 