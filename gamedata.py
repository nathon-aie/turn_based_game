from kivy.uix.screenmanager import Scale

SKILLS = {
    "Punch": {"type": "attack", "value": 10},
    "Fireball": {"type": "attack", "value": 25},
    "Heal": {"type": "heal", "value": 30},
    "Slash": {"type": "attack", "value": 15},
    "Nuke": {"type": "attack", "value": 444},
    "Dimension Slash": {"type": "attack", "value": 100},
    "Ambatakum": {"type": "heal", "value": 100},
    "Demacia": {"type": "attack", "value": 999},
}

HEROES = {
    "Mambo": {
        "hp": 100,
        "atk": 25,
        "skills": ["Demacia", "Dimension Slash", "Heal", "Nuke"],
    },
}

ENEMIES = {
    "Noob Slayer": {"hp": 100, "atk": 10, "skills": ["Punch"]},
    "Goblin Slayer": {"hp": 200, "atk": 15, "skills": ["Fireball", "Slash"]},
    "God Slayer": {"hp": 500, "atk": 30, "skills": ["Nuke"]},
    "Anuthin": {"hp": 250, "atk": 20, "skills": ["Punch", "Fireball", "Slash"]},
    "Anuthin Slayer": {"hp": 700, "atk": 18, "skills": ["Nuke"]},
    "P'tae": {
        "hp": 1000,
        "atk": 50,
        "skills": ["Punch", "Ambatakum", "Dimension Slash", "Nuke"],
    },
}

ITEMS = {
    "Potion": {
        "type": "heal",
        "value": 50,
        "description": "Restores 50 HP.\nA simple red potion.",
    },
    "Bomb": {
        "type": "attack",
        "value": 30,
        "description": "Deals 30 DMG to enemy.\nExplosive!",
    },
    "Super Potion": {
        "type": "heal",
        "value": 100,
        "description": "Restores 100 HP.\nA stronger potion.",
    },
}
