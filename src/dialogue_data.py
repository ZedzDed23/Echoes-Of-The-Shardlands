# src/dialogue_data.py
dialogues = {
    "sage_intro": {
        "npc_text": "Greetings, wanderer. These Shardlands are full of echoes from forgotten times. What brings you to this forsaken place?",
        "player_options": [
            {"text": "I'm looking for answers about this place.", "next_node": "sage_answers_place"},
            {"text": "Who are you?", "next_node": "sage_who_are_you"},
            {"text": "Just exploring. (Leave)", "action": "end_dialogue"}
        ]
    },
    "sage_answers_place": {
        "npc_text": "Answers are as fragmented as the Shards themselves. Seek the Great Archive, though its path is perilous.",
        "player_options": [
            {"text": "Tell me more about the Great Archive.", "next_node": "sage_great_archive_info"},
            {"text": "Thank you. (Leave)", "action": "end_dialogue"}
        ]
    },
    "sage_who_are_you": {
        "npc_text": "I am but a keeper of tales, a listener to the whispers of the Shards. Many call me the Sage.",
        "player_options": [
            {"text": "Can you help me?", "next_node": "sage_can_help"},
            {"text": "Interesting. (Leave)", "action": "end_dialogue"}
        ]
    },
    "sage_great_archive_info": {
        "npc_text": "The Archive is not a place, but a confluence of memories. It is said that those who are sufficiently attuned can find their way. Be wary, for not all memories are kind.",
        "player_options": [
            {"text": "I understand. (Leave)", "action": "end_dialogue"}
        ]
    },
    "sage_can_help": {
        "npc_text": "Help takes many forms. Perhaps the Shards you collect will guide your path better than any words I offer. Observe, listen, and remember.",
        "player_options": [
            {"text": "I will. Thank you. (Leave)", "action": "end_dialogue"}
        ]
    }
    # Add more dialogue nodes as needed
}
