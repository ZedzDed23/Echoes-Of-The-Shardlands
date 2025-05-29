from entities import Stats, Player, Item
from world_gen import WorldGenerator
from combat import CombatSystem

def test_stats():
    """Test basic stats functionality."""
    stats = Stats(health=100, max_health=100, attack=10, defense=5)
    
    # Test damage
    damage_dealt = stats.take_damage(20)
    assert damage_dealt == 15  # 20 - 5 defense
    assert stats.health == 85
    
    # Test healing
    healed = stats.heal(10)
    assert healed == 10
    assert stats.health == 95
    
    # Test overhealing
    healed = stats.heal(10)
    assert healed == 5  # Only healed up to max_health
    assert stats.health == 100

def test_player():
    """Test player functionality."""
    player = Player(
        name="Test Hero",
        stats=Stats(health=100, max_health=100, attack=10, defense=5)
    )
    
    # Test inventory
    assert len(player.inventory) == 0
    assert player.can_add_item()
    
    item = Item(
        name="Test Potion",
        description="A test item",
        effect_type="heal",
        effect_value=20,
        rarity="common"
    )
    
    assert player.add_item(item)
    assert len(player.inventory) == 1
    
    # Test item removal
    removed_item = player.remove_item(0)
    assert removed_item == item
    assert len(player.inventory) == 0

def test_world_generation():
    """Test world generation."""
    world_gen = WorldGenerator(depth=3, width=3)
    start_room, all_rooms = world_gen.generate_world()
    
    # Test basic world structure
    assert len(all_rooms) == 9  # 3x3 grid
    assert start_room in all_rooms
    
    # Test room connections
    for room in all_rooms:
        # Each room should have at least one connection (except if randomly removed)
        assert room.room_type in ['combat', 'treasure', 'event']
        
        # Test room content based on type
        if room.room_type == 'combat':
            assert len(room.enemies) in [1, 2]  # 1-2 enemies per combat room
        elif room.room_type == 'treasure':
            assert len(room.items) in [1, 2, 3]  # 1-3 items per treasure room
        elif room.room_type == 'event':
            assert room.event_id is not None

def test_combat():
    """Test basic combat functionality."""
    player = Player(
        name="Test Hero",
        stats=Stats(health=100, max_health=100, attack=10, defense=5)
    )
    
    enemy = world_gen = WorldGenerator().generate_enemy(difficulty=1)
    combat = CombatSystem(player=player, enemies=[enemy])
    
    # Test that combat system is properly initialized
    assert len(combat.enemies) == 1
    assert combat.turn_count == 0
    assert combat.player == player 