from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
from entities import Player, Item
from utils import print_colored, get_input, roll_dice, chance, Fore, format_command_help

@dataclass
class EventChoice:
    description: str
    success_text: str
    failure_text: str
    success_chance: float = 1.0
    required_item: Optional[str] = None
    stat_check: Optional[Tuple[str, int]] = None  # (stat_name, required_value)
    shard_reward: int = 10  # Base reward for this choice
    special_reward: Optional[str] = None  # Special reward type if any

@dataclass
class Event:
    id: str
    title: str
    description: str
    choices: List[EventChoice]
    on_success: Optional[Callable[[Player], str]] = None
    on_failure: Optional[Callable[[Player], str]] = None
    difficulty: int = 1  # Event difficulty level

class EventSystem:
    def __init__(self):
        self.events = self._initialize_events()
        
    def _initialize_events(self) -> Dict[str, Event]:
        """Initialize all possible events."""
        events = {}
        
        # Event 1: Mysterious Shrine
        events['event_1'] = Event(
            id='event_1',
            title="Mysterious Shrine",
            description="You encounter a crystalline shrine pulsing with energy. "
                       "Ancient runes suggest it might grant power... or drain it.",
            difficulty=1,
            choices=[
                EventChoice(
                    description="Touch the shrine",
                    success_text="The shrine's energy flows into you, invigorating your being!",
                    failure_text="The shrine drains some of your life force!",
                    success_chance=0.6,
                    shard_reward=20,
                    special_reward="health_boost"
                ),
                EventChoice(
                    description="Study the runes carefully",
                    success_text="You decipher the runes and safely harness the shrine's power!",
                    failure_text="The runes blur before your eyes, yielding no insights.",
                    success_chance=0.8,
                    shard_reward=15,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Leave it alone",
                    success_text="You wisely choose to avoid the mysterious shrine.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )
        
        # Event 2: Trapped Chest
        events['event_2'] = Event(
            id='event_2',
            title="Trapped Chest",
            description="A ornate chest sits before you, but you notice subtle signs of a trap.",
            difficulty=2,
            choices=[
                EventChoice(
                    description="Carefully disarm the trap",
                    success_text="You successfully disarm the trap and claim the treasure!",
                    failure_text="The trap triggers, causing damage!",
                    success_chance=0.5,
                    shard_reward=25,
                    special_reward="treasure"
                ),
                EventChoice(
                    description="Force it open quickly",
                    success_text="Your quick action prevents the trap from fully triggering!",
                    failure_text="The trap triggers with full force!",
                    success_chance=0.3,
                    shard_reward=35,
                    special_reward="treasure"
                ),
                EventChoice(
                    description="Look for a key",
                    success_text="You find a hidden key and open the chest safely!",
                    failure_text="You find nothing useful after searching.",
                    success_chance=0.7,
                    shard_reward=15,
                    special_reward="treasure"
                )
            ]
        )
        
        # Event 3: Memory Echo
        events['event_3'] = Event(
            id='event_3',
            title="Memory Echo",
            description="A shimmering apparition appears, offering to share ancient knowledge.",
            difficulty=1,
            choices=[
                EventChoice(
                    description="Accept the knowledge",
                    success_text="The memories flow into your mind, granting insight!",
                    failure_text="The foreign memories cause temporary confusion!",
                    success_chance=0.7,
                    shard_reward=20,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Try to absorb only specific memories",
                    success_text="You successfully filter and absorb useful knowledge!",
                    failure_text="The memories become jumbled and fade away.",
                    success_chance=0.5,
                    shard_reward=30,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Decline politely",
                    success_text="The apparition nods in understanding and fades away.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )
        
        # Event 4: Unstable Crystal
        events['event_4'] = Event(
            id='event_4',
            title="Unstable Crystal",
            description="A large crystal pulses with unstable energy. It might contain "
                       "valuable Memory Shards, but looks dangerous.",
            difficulty=3,
            choices=[
                EventChoice(
                    description="Attempt to stabilize it",
                    success_text="You successfully stabilize the crystal and extract its power!",
                    failure_text="The crystal shatters, releasing harmful energy!",
                    success_chance=0.4,
                    shard_reward=40,
                    special_reward="power"
                ),
                EventChoice(
                    description="Break it quickly",
                    success_text="You break it and gather the shards before the energy disperses!",
                    failure_text="The crystal explodes violently!",
                    success_chance=0.6,
                    shard_reward=30,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Leave it alone",
                    success_text="You wisely avoid the unstable crystal.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )
        
        # Event 5: Time Anomaly
        events['event_5'] = Event(
            id='event_5',
            title="Time Anomaly",
            description="You encounter a strange temporal distortion in the air.",
            difficulty=2,
            choices=[
                EventChoice(
                    description="Step through",
                    success_text="You emerge in a favorable moment!",
                    failure_text="The temporal shift disorients you!",
                    success_chance=0.5,
                    shard_reward=35,
                    special_reward="time"
                ),
                EventChoice(
                    description="Study the anomaly",
                    success_text="You learn something about the nature of the Shardlands!",
                    failure_text="The anomaly collapses without yielding insights.",
                    success_chance=0.8,
                    shard_reward=20,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Wait for it to dissipate",
                    success_text="The anomaly fades harmlessly away.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )
        
        return events
        
    def apply_special_reward(self, reward_type: str, player: Player) -> str:
        """Apply a special reward effect and return a description."""
        if reward_type == "health_boost":
            heal_amount = 20 + roll_dice(10, 30)
            player.stats.heal(heal_amount)
            return f"You are healed for {heal_amount} HP!"
            
        elif reward_type == "knowledge":
            bonus_shards = roll_dice(10, 25)
            player.memory_shards += bonus_shards
            return f"You gain {bonus_shards} additional Memory Shards from the knowledge!"
            
        elif reward_type == "treasure":
            bonus_shards = roll_dice(20, 40)
            player.memory_shards += bonus_shards
            return f"The treasure contained {bonus_shards} Memory Shards!"
            
        elif reward_type == "power":
            attack_boost = roll_dice(2, 5)
            player.stats.attack += attack_boost
            return f"Your attack power increases by {attack_boost}!"
            
        elif reward_type == "shards":
            bonus_shards = roll_dice(30, 50)
            player.memory_shards += bonus_shards
            return f"You gather {bonus_shards} Memory Shards from the crystal!"
            
        elif reward_type == "time":
            heal_amount = player.stats.max_health // 2
            player.stats.heal(heal_amount)
            return f"Time reverses around your wounds, healing you for {heal_amount} HP!"
            
        return "No special effect."
        
    def handle_event(self, event_id: str, player: Player) -> bool:
        """Handle an event. Returns True if player survived the event."""
        if event_id not in self.events:
            print_colored("Error: Event not found!", Fore.RED)
            return True
            
        event = self.events[event_id]
        
        print_colored(f"\n=== {event.title} ===", Fore.CYAN, bold=True)
        print(f"\n{event.description}\n")
        
        # Display choices
        print("Choices:")
        for i, choice in enumerate(event.choices, 1):
            print(f"{i}. {choice.description}")
            
        # Available commands for event choices
        commands = {
            'choose': [str(i) for i in range(1, len(event.choices) + 1)]
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
        
        if args and args[0] in commands['choose']:
            choice_idx = int(args[0]) - 1
        else:
            choice_idx = int(get_input(
                "Choose your action (number)",
                valid_options=[str(i) for i in range(1, len(event.choices) + 1)]
            )) - 1
        
        chosen = event.choices[choice_idx]
        
        # Check if choice succeeds
        success = chance(chosen.success_chance)
        
        if success:
            print_colored(f"\n{chosen.success_text}", Fore.GREEN)
            
            # Calculate reward
            base_reward = chosen.shard_reward
            risk_bonus = int((1.0 - chosen.success_chance) * 20)
            difficulty_bonus = event.difficulty * 5
            total_reward = base_reward + risk_bonus + difficulty_bonus
            
            player.memory_shards += total_reward
            
            # Show reward breakdown
            print_colored("\nRewards:", Fore.YELLOW)
            print(f"Base Reward: {base_reward} Memory Shards")
            if risk_bonus > 0:
                print(f"Risk Bonus: +{risk_bonus} Memory Shards")
            print(f"Difficulty Bonus: +{difficulty_bonus} Memory Shards")
            print_colored(f"Total: +{total_reward} Memory Shards!", Fore.YELLOW, bold=True)
            
            # Apply special reward if any
            if chosen.special_reward:
                result = self.apply_special_reward(chosen.special_reward, player)
                print_colored(result, Fore.CYAN)
                
            if event.on_success:
                result = event.on_success(player)
                print_colored(result, Fore.YELLOW)
        else:
            print_colored(f"\n{chosen.failure_text}", Fore.RED)
            if event.on_failure:
                result = event.on_failure(player)
                print_colored(result, Fore.YELLOW)
                
            # Small consolation reward for trying
            consolation = 5
            player.memory_shards += consolation
            print_colored(f"\nConsolation: +{consolation} Memory Shards", Fore.YELLOW)
                
        return True  # For now, events can't kill the player 