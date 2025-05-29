import random
from typing import Dict, List, Optional, Tuple
from entities import Room, Enemy, Item, Stats
from utils import chance

class WorldGenerator:
    def __init__(self, depth: int = 5, width: int = 5):
        self.depth = depth
        self.width = width
        self.room_types = ['combat', 'treasure', 'event']
        self.directions = ['north', 'south', 'east', 'west']
        self.mini_boss_defeated = 0  # Track number of mini-bosses defeated
        self.next_mini_boss = random.randint(10, 15)  # Next mini-boss floor
        
    def get_enemy_abilities(self, enemy_type: str, difficulty: int) -> List[str]:
        """Get special abilities for an enemy based on type and difficulty."""
        base_abilities = {
            'Shard Golem': ['attack'],  # Tank
            'Crystal Spider': ['attack'],  # Glass cannon
            'Shadow Wraith': ['attack'],  # Balanced damage
            'Memory Eater': ['attack'],  # Balanced+
            'Void Stalker': ['attack'],  # Strong all around
        }
        
        # Special abilities unlocked at higher difficulties
        special_abilities = {
            'Shard Golem': {
                3: ['attack', 'shield'],  # Gains temporary defense boost
                5: ['attack', 'shield', 'regenerate'],  # Heals over time
            },
            'Crystal Spider': {
                3: ['attack', 'double_strike'],  # Two attacks in one turn
                5: ['attack', 'double_strike', 'poison'],  # DoT effect
            },
            'Shadow Wraith': {
                3: ['attack', 'life_drain'],  # Damage + self heal
                5: ['attack', 'life_drain', 'curse'],  # Reduces player defense
            },
            'Memory Eater': {
                3: ['attack', 'confuse'],  # Chance to make player miss
                5: ['attack', 'confuse', 'mind_blast'],  # High damage skill
            },
            'Void Stalker': {
                3: ['attack', 'void_strike'],  # Ignores some defense
                5: ['attack', 'void_strike', 'darkness'],  # Reduces player accuracy
            }
        }
        
        # Get the highest tier of abilities unlocked at current difficulty
        abilities = base_abilities[enemy_type].copy()
        for diff_req, diff_abilities in special_abilities[enemy_type].items():
            if difficulty >= diff_req:
                abilities = diff_abilities.copy()
                
        return abilities

    def generate_mini_boss(self, difficulty: int) -> Enemy:
        """Generate a mini-boss enemy with enhanced stats and abilities."""
        mini_boss_types = [
            # (name, health_mult, attack_mult, defense_mult, abilities)
            ('Crystal Overlord', 2.0, 1.8, 1.5, 
             ['attack', 'crystal_burst', 'summon_shards', 'overcharge']),
            ('Void Harbinger', 1.8, 2.0, 1.3, 
             ['attack', 'void_explosion', 'shadow_clone', 'death_mark']),
            ('Memory Sovereign', 1.7, 1.7, 1.7, 
             ['attack', 'mind_shatter', 'temporal_shift', 'essence_drain']),
        ]
        
        name, health_mult, attack_mult, defense_mult, abilities = random.choice(mini_boss_types)
        
        # Mini-boss stats scale even higher than normal enemies
        base_stats = {
            'health': int(50 * (difficulty ** 1.6) * health_mult),
            'attack': int(15 * (difficulty ** 1.4) * attack_mult),
            'defense': int(5 * (difficulty ** 1.3) * defense_mult)
        }
        
        # Less random variation for mini-bosses to ensure consistent challenge
        variation = 0.05 + (difficulty * 0.01)
        for stat in base_stats:
            base_stats[stat] = int(base_stats[stat] * random.uniform(1 - variation, 1 + variation))
            
        base_stats['max_health'] = base_stats['health']
        stats = Stats(**base_stats)
        
        # Mini-bosses have guaranteed better loot
        loot_table = {
            'health_potion': 1.0,  # Guaranteed health potion
            'damage_crystal': 0.8,
            'legendary_item': 0.3  # Chance for legendary item
        }
        
        return Enemy(
            name=f"Mini-Boss: {name} (Lvl {difficulty})",
            stats=stats,
            level=difficulty,
            attack_pattern=abilities,
            loot_table=loot_table,
            experience_value=difficulty * 25,  # More XP than regular enemies
            is_mini_boss=True
        )
        
    def generate_enemy(self, difficulty: int) -> Enemy:
        """Generate an enemy based on difficulty level."""
        # Apply mini-boss difficulty scaling
        scaled_difficulty = difficulty + self.mini_boss_defeated  # Each mini-boss increases effective difficulty
        
        enemy_types = [
            # (name, health_mult, attack_mult, defense_mult, rarity)
            ('Shard Golem',    1.2, 1.0, 1.4, 'common'),
            ('Crystal Spider', 0.8, 1.3, 0.7, 'common'),
            ('Shadow Wraith',  1.0, 1.2, 0.8, 'uncommon'),
            ('Memory Eater',   1.1, 1.1, 1.0, 'uncommon'),
            ('Void Stalker',   1.3, 1.4, 1.1, 'rare')
        ]
        
        # Select enemy type, with higher difficulties favoring stronger enemies
        if scaled_difficulty >= 3 and chance(0.3):
            possible_types = [e for e in enemy_types if e[4] == 'rare']
        elif scaled_difficulty >= 2 and chance(0.5):
            possible_types = [e for e in enemy_types if e[4] in ['uncommon', 'rare']]
        else:
            possible_types = enemy_types
            
        name, health_mult, attack_mult, defense_mult, _ = random.choice(possible_types)
        
        # Base stats scale exponentially with difficulty
        base_stats = {
            'health': int(25 * (scaled_difficulty ** 1.5) * health_mult),
            'attack': int(8 * (scaled_difficulty ** 1.3) * attack_mult),
            'defense': int(3 * (scaled_difficulty ** 1.2) * defense_mult)
        }
        
        # Add random variation
        variation = 0.1 + (scaled_difficulty * 0.02)
        for stat in base_stats:
            base_stats[stat] = int(base_stats[stat] * random.uniform(1 - variation, 1 + variation))
        
        # Ensure minimum stats
        base_stats['health'] = max(15, base_stats['health'])
        base_stats['attack'] = max(5, base_stats['attack'])
        base_stats['defense'] = max(1, base_stats['defense'])
        base_stats['max_health'] = base_stats['health']
        
        stats = Stats(**base_stats)
        
        # Get abilities based on enemy type and difficulty
        abilities = self.get_enemy_abilities(name, scaled_difficulty)
        
        # Higher difficulty enemies have better loot chances
        loot_table = {
            'health_potion': 0.3 + (scaled_difficulty * 0.05),
            'damage_crystal': 0.2 + (scaled_difficulty * 0.05)
        }
        
        return Enemy(
            name=f"Lvl {scaled_difficulty} {name}",
            stats=stats,
            level=scaled_difficulty,
            attack_pattern=abilities,
            loot_table=loot_table,
            experience_value=scaled_difficulty * 10
        )
    
    def generate_item(self, rarity: str = 'common') -> Item:
        """Generate a random item with given rarity."""
        rarity_multiplier = {
            'common': 1.0,
            'uncommon': 1.5,
            'rare': 2.0,
            'legendary': 3.0
        }
        
        item_types = [
            ('Health Potion', 'heal', 20, 'restores {} health'),
            ('Damage Crystal', 'damage', 15, 'deals up to {} damage'),
            ('Shield Shard', 'defense', 5, 'temporarily grants {} defense'),
            ('Power Fragment', 'attack', 3, 'temporarily grants {} attack')
        ]
        
        name_base, effect_type, base_value, desc_template = random.choice(item_types)
        value = int(base_value * rarity_multiplier[rarity])
        
        # Adjust description based on effect type
        if effect_type in ['attack', 'defense']:
            target = 'self'
        else:
            target = 'target'
            
        description = f"A {rarity} item that {desc_template.format(value)} to {target}"
        
        return Item(
            name=f"{rarity.capitalize()} {name_base}",
            description=description,
            effect_type=effect_type,
            effect_value=value,
            rarity=rarity,
            durability=random.randint(3, 5) if chance(0.3) else None
        )
    
    def generate_room_description(self, room_type: str) -> str:
        """Generate a description for a room based on its type."""
        descriptions = {
            'combat': [
                "A dark chamber echoes with distant growls.",
                "Crystal formations cast eerie shadows on the walls.",
                "The air crackles with hostile energy."
            ],
            'treasure': [
                "Glittering shards catch your eye in the corners.",
                "A peaceful sanctuary filled with crystalline formations.",
                "Ancient pedestals hold mysterious artifacts."
            ],
            'event': [
                "Strange symbols pulse with an inner light.",
                "The air shimmers with potential possibilities.",
                "Time seems to flow differently in this space."
            ]
        }
        return random.choice(descriptions[room_type])
    
    def generate_room(self, difficulty: int) -> Room:
        """Generate a single room with appropriate content."""
        room_type = random.choice(self.room_types)
        description = self.generate_room_description(room_type)
        
        room = Room(room_type=room_type, description=description)
        
        # Check if this should be a mini-boss room
        current_floor = (difficulty - 1) // 2  # Approximate floor number
        if current_floor == self.next_mini_boss:
            room.room_type = 'mini_boss'
            room.description = self.generate_mini_boss_description()
            room.enemies = [self.generate_mini_boss(difficulty)]
            self.mini_boss_defeated += 1
            self.next_mini_boss = current_floor + random.randint(10, 15)
        elif room_type == 'combat':
            num_enemies = random.randint(1, 2)
            room.enemies = [self.generate_enemy(difficulty) for _ in range(num_enemies)]
        elif room_type == 'treasure':
            num_items = random.randint(1, 3)
            rarities = ['common'] * 6 + ['uncommon'] * 3 + ['rare'] * 1
            room.items = [self.generate_item(random.choice(rarities)) for _ in range(num_items)]
        elif room_type == 'event':
            room.event_id = f"event_{random.randint(1, 5)}"
            
        return room
    
    def generate_mini_boss_description(self) -> str:
        """Generate a description for a mini-boss room."""
        descriptions = [
            "The air grows heavy with malevolent energy as an ancient guardian stirs...",
            "Crystal formations pulse with an ominous rhythm, heralding a powerful presence...",
            "The very walls seem to tremble before the might of what awaits you...",
            "An otherworldly silence falls as you sense an overwhelming force ahead..."
        ]
        return random.choice(descriptions)
    
    def generate_world(self) -> Tuple[Room, List[Room]]:
        """Generate the complete game world and return (start_room, all_rooms)."""
        all_rooms = []
        
        # Create grid of rooms
        grid = [[self.generate_room(max(1, (x + y) // 2)) 
                for x in range(self.width)] 
                for y in range(self.depth)]
        
        # Connect rooms
        for y in range(self.depth):
            for x in range(self.width):
                current = grid[y][x]
                all_rooms.append(current)
                
                # Connect to east room
                if x < self.width - 1:
                    current.add_connection('east', grid[y][x + 1])
                
                # Connect to south room
                if y < self.depth - 1:
                    current.add_connection('south', grid[y + 1][x])
        
        # Remove some connections to make it more interesting
        for room in all_rooms:
            for direction in list(room.connections.keys()):
                if chance(0.2):  # 20% chance to remove each connection
                    connected_room = room.connections[direction]
                    reverse_dir = {'north': 'south', 'south': 'north', 
                                 'east': 'west', 'west': 'east'}[direction]
                    
                    del room.connections[direction]
                    if reverse_dir in connected_room.connections:
                        del connected_room.connections[reverse_dir]
        
        return grid[0][0], all_rooms  # Start room is top-left 

    def generate_legendary_item(self) -> Item:
        """Generate a special legendary item."""
        legendary_items = [
            {
                'name': 'Phoenix Elixir',
                'description': 'A legendary potion that fully restores health',
                'effect_type': 'heal',
                'effect_value': 999,  # Full heal
                'special_effect': 'resurrect'  # Could be used for future mechanics
            },
            {
                'name': 'Void Shard',
                'description': 'A crystal infused with pure void energy',
                'effect_type': 'damage',
                'effect_value': 50
            },
            {
                'name': 'Time Fragment',
                'description': 'A crystallized moment of time',
                'effect_type': 'heal',
                'effect_value': 100,
                'special_effect': 'time_stop'  # Could be used for future mechanics
            },
            {
                'name': 'Memory Crystal',
                'description': 'Contains the memories of a powerful being',
                'effect_type': 'buff',
                'effect_value': 20,
                'special_effect': 'skill_boost'
            },
            {
                'name': 'Eternity Shard',
                'description': 'A fragment of endless possibility',
                'effect_type': 'special',
                'effect_value': 0,
                'special_effect': 'reroll'  # Could be used for future mechanics
            }
        ]
        
        item_data = random.choice(legendary_items)
        return Item(
            name=item_data['name'],
            description=item_data['description'],
            effect_type=item_data['effect_type'],
            effect_value=item_data['effect_value'],
            rarity='legendary'
        ) 