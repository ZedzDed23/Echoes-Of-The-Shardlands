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

        # ── New encounters ───────────────────────────────────────────────────

        # Event 6: Ancient Inscription
        events['event_6'] = Event(
            id='event_6',
            title="Ancient Inscription",
            description="Carved deep into the stone wall: runes that predate the Shardlands "
                        "themselves. The text pulses faintly, as if still alive.",
            difficulty=1,
            choices=[
                EventChoice(
                    description="Read the inscription aloud",
                    success_text="The words resonate through the chamber, unlocking a hidden cache!",
                    failure_text="The words twist your tongue; a ward triggers and stings you.",
                    success_chance=0.65,
                    shard_reward=18,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Copy the runes into memory",
                    success_text="The pattern clicks — a burst of insight fills your mind.",
                    failure_text="The runes shimmer and rearrange, defying your recall.",
                    success_chance=0.8,
                    shard_reward=12,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Ignore it and press on",
                    success_text="You walk past, unburdened.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=3
                )
            ]
        )

        # Event 7: Shard Vein
        events['event_7'] = Event(
            id='event_7',
            title="Shard Vein",
            description="A vein of raw Memory Shards runs through the floor. "
                        "The crystals hum with latent power — prying them loose will take effort.",
            difficulty=2,
            choices=[
                EventChoice(
                    description="Mine carefully with steady hands",
                    success_text="You extract a generous cluster of pristine shards!",
                    failure_text="The vein fractures — most shards crumble to dust.",
                    success_chance=0.7,
                    shard_reward=30,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Strike fast and hard",
                    success_text="The vein shatters spectacularly, showering you with shards!",
                    failure_text="The shock wave rebounds painfully — and the shards scatter.",
                    success_chance=0.4,
                    shard_reward=55,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Leave the vein intact",
                    success_text="Some things are best left undisturbed.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )

        # Event 8: Ghost Echo (fallen adventurer's memory)
        events['event_8'] = Event(
            id='event_8',
            title="Ghost Echo",
            description="A translucent silhouette flickers before you — the memory-ghost of a "
                        "fallen adventurer, still clutching a weapon that no longer exists.",
            difficulty=2,
            choices=[
                EventChoice(
                    description="Speak the adventurer's name (guess)",
                    success_text="'Yes…' it breathes, dissolving peacefully — leaving their strength in you.",
                    failure_text="The ghost recoils, then lashes out before fading.",
                    success_chance=0.45,
                    shard_reward=25,
                    special_reward="power"
                ),
                EventChoice(
                    description="Offer a moment of silence",
                    success_text="Grateful, the echo gifts you a fragment of its remaining will.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=15,
                    special_reward="health_boost"
                ),
                EventChoice(
                    description="Back away slowly",
                    success_text="The ghost watches you go, motionless.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=4
                )
            ]
        )

        # Event 9: Dark Pact
        events['event_9'] = Event(
            id='event_9',
            title="Dark Pact",
            description="A shadowed altar glows with a sickly light. An inscription reads: "
                        "'OFFER BLOOD — RECEIVE POWER.' The choice is entirely yours.",
            difficulty=3,
            choices=[
                EventChoice(
                    description="Make the pact (sacrifice 25 HP for great power)",
                    success_text="Pain courses through you — then raw strength follows!",
                    failure_text="The pact rejects you, draining more than promised.",
                    success_chance=0.75,
                    shard_reward=10,
                    special_reward="dark_pact"
                ),
                EventChoice(
                    description="Deface the altar",
                    success_text="The altar cracks, releasing a burst of freed energy!",
                    failure_text="The altar retaliates with a venomous surge.",
                    success_chance=0.5,
                    shard_reward=35,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Walk away",
                    success_text="Wisdom is its own reward.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )

        # Event 10: Crystal Font
        events['event_10'] = Event(
            id='event_10',
            title="Crystal Font",
            description="A basin carved from living crystal fills slowly with luminous water. "
                        "It smells of lightning and distant rain.",
            difficulty=1,
            choices=[
                EventChoice(
                    description="Drink deeply",
                    success_text="Cool, radiant energy spreads through every wound.",
                    failure_text="The water burns — it was not meant for you.",
                    success_chance=0.75,
                    shard_reward=10,
                    special_reward="time"
                ),
                EventChoice(
                    description="Splash it on your wounds only",
                    success_text="Careful application closes the worst of your injuries.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=8,
                    special_reward="health_boost"
                ),
                EventChoice(
                    description="Fill a container to take with you",
                    success_text="The water holds its glow — a useful supply for later.",
                    failure_text="The water turns inert the moment it leaves the basin.",
                    success_chance=0.6,
                    shard_reward=12,
                    special_reward="carry_water"
                )
            ]
        )

        # Event 11: Shadow Portal
        events['event_11'] = Event(
            id='event_11',
            title="Shadow Portal",
            description="A tear in the fabric of the Shardlands hangs before you — "
                        "dark around the edges, bright at the centre. It smells of ozone and old iron.",
            difficulty=3,
            choices=[
                EventChoice(
                    description="Step through the portal",
                    success_text="You emerge deeper in the dungeon, shards raining around you!",
                    failure_text="The portal spits you out — battered, disoriented, and hurt.",
                    success_chance=0.5,
                    shard_reward=50,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Toss a pebble through to test it",
                    success_text="The pebble returns as a shard cluster — you take it!",
                    failure_text="The pebble does not return. Neither would you.",
                    success_chance=0.7,
                    shard_reward=20,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Seal the portal",
                    success_text="The Shardlands trembles gratefully — something rewards your caution.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=18,
                    special_reward="health_boost"
                )
            ]
        )

        # Event 12: Forgotten Cache
        events['event_12'] = Event(
            id='event_12',
            title="Forgotten Cache",
            description="Behind a loose stone you find a hollow containing dust, bones, "
                        "and — underneath it all — carefully wrapped bundles.",
            difficulty=1,
            choices=[
                EventChoice(
                    description="Unwrap the bundles",
                    success_text="Preserved supplies! Potions, shards, and a useful trinket.",
                    failure_text="The contents crumble the moment air touches them.",
                    success_chance=0.8,
                    shard_reward=22,
                    special_reward="treasure"
                ),
                EventChoice(
                    description="Search the bones for clues",
                    success_text="A journal fragment describes a secret passage nearby!",
                    failure_text="The bones hold no answers — only dust.",
                    success_chance=0.55,
                    shard_reward=15,
                    special_reward="knowledge"
                ),
                EventChoice(
                    description="Leave everything as found",
                    success_text="Respect for the dead has its own quiet value.",
                    failure_text="",
                    success_chance=1.0,
                    shard_reward=5
                )
            ]
        )

        # Event 13: Echoing Voice
        events['event_13'] = Event(
            id='event_13',
            title="Echoing Voice",
            description="From somewhere ahead — or behind, it is impossible to say — "
                        "a voice calls your name. It knows things it should not.",
            difficulty=2,
            choices=[
                EventChoice(
                    description="Answer the voice",
                    success_text="A resonant warmth fills you — the voice imparts a fragment of power.",
                    failure_text="Answering draws something malevolent; it grazes your mind before vanishing.",
                    success_chance=0.6,
                    shard_reward=25,
                    special_reward="power"
                ),
                EventChoice(
                    description="Trace the source",
                    success_text="You find a cluster of resonant crystals vibrating with sound-energy.",
                    failure_text="The voice leads you in circles — you waste precious time.",
                    success_chance=0.5,
                    shard_reward=30,
                    special_reward="shards"
                ),
                EventChoice(
                    description="Cover your ears and walk on",
                    success_text="The voice fades to silence behind you.",
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
            return f"You gather {bonus_shards} Memory Shards!"
            
        elif reward_type == "time":
            heal_amount = player.stats.max_health // 2
            player.stats.heal(heal_amount)
            return f"Time reverses around your wounds, healing you for {heal_amount} HP!"

        elif reward_type == "dark_pact":
            damage = 25
            attack_boost = roll_dice(4, 8)
            defense_boost = roll_dice(2, 4)
            player.stats.health = max(1, player.stats.health - damage)
            player.stats.attack += attack_boost
            player.stats.defense += defense_boost
            return (f"You lose {damage} HP but gain +{attack_boost} ATK "
                    f"and +{defense_boost} DEF from the pact!")

        elif reward_type == "carry_water":
            # Treated as a moderate heal when successfully bottled
            heal_amount = roll_dice(15, 25)
            player.stats.heal(heal_amount)
            return f"The crystal water restores {heal_amount} HP on contact!"
            
        return "No special effect."
        
    def handle_event(self, event_id: str, player: Player) -> bool:
        """Handle an event. Returns True if player survived the event."""
        if event_id not in self.events:
            print_colored("Error: Event not found!", Fore.RED)
            return True
            
        event = self.events[event_id]
        
        print_colored(f"\n{'═' * 60}", Fore.YELLOW)
        print_colored(f"  *** {event.title.upper()} ***", Fore.YELLOW, bold=True)
        print_colored(f"{'═' * 60}", Fore.YELLOW)
        print(f"\n{event.description}\n")
        
        # Display choices
        print_colored("What do you do?", Fore.GREEN)
        for i, choice in enumerate(event.choices, 1):
            print(f"  {i}. {choice.description}")
            
        # Available commands for event choices
        commands = {
            'choose': [str(i) for i in range(1, len(event.choices) + 1)]
        }
        
        action = get_input(
            f"\nChoice ({format_command_help(commands)})",
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
                "Enter choice number",
                valid_options=[str(i) for i in range(1, len(event.choices) + 1)]
            )) - 1
        
        chosen = event.choices[choice_idx]
        
        # Check if choice succeeds
        success = chance(chosen.success_chance)
        
        if success:
            print_colored(f"\n> {chosen.success_text}", Fore.GREEN)
            
            # Calculate reward
            base_reward = chosen.shard_reward
            risk_bonus = int((1.0 - chosen.success_chance) * 20)
            difficulty_bonus = event.difficulty * 5
            total_reward = base_reward + risk_bonus + difficulty_bonus
            
            player.memory_shards += total_reward
            
            # Show reward breakdown
            print_colored("\nRewards:", Fore.YELLOW)
            print(f"  Base:             +{base_reward} Memory Shards")
            if risk_bonus > 0:
                print(f"  Risk bonus:       +{risk_bonus} Memory Shards")
            print(f"  Difficulty bonus: +{difficulty_bonus} Memory Shards")
            print_colored(f"  Total:            +{total_reward} Memory Shards", Fore.YELLOW, bold=True)
            
            # Apply special reward if any
            if chosen.special_reward:
                result = self.apply_special_reward(chosen.special_reward, player)
                print_colored(f"\n> {result}", Fore.CYAN)
                
            if event.on_success:
                result = event.on_success(player)
                print_colored(result, Fore.YELLOW)
        else:
            print_colored(f"\n> {chosen.failure_text}", Fore.RED)
            if event.on_failure:
                result = event.on_failure(player)
                print_colored(result, Fore.YELLOW)
                
            # Small consolation reward for trying
            consolation = 5
            player.memory_shards += consolation
            print_colored(f"\n  Consolation: +{consolation} Memory Shards", Fore.YELLOW)
                
        return True  # For now, events can't kill the player 