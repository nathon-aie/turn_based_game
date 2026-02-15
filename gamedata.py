SKILLS = {
    "Punch": {"type": "attack", "value": 10},
    "Fireball": {"type": "attack", "value": 25},
    "Heal": {"type": "heal", "value": 30},
    "Slash": {"type": "attack", "value": 15},
    "Nuke": {"type": "attack", "value": 999},
}

HEROES = {
    "Mambo": {
        "hp": 100,
        "atk": 10,
        "skills": ["Punch", "Fireball", "Heal", "Nuke"],
    },
}

ENEMIES = {
    "Noob Slayer": {"hp": 100, "atk": 10, "skills": ["Punch"]},
    "Goblin Slayer": {"hp": 200, "atk": 15, "skills": ["Fireball", "Slash"]},
    "God Slayer": {"hp": 500, "atk": 30, "skills": ["Nuke"]},
    "Anuthin": {"hp": 250, "atk": 20, "skills": ["Punch", "Fireball", "Slash"]},
    "Anuthin Slayer": {"hp": 700, "atk": 18, "skills": ["Nuke"]},
}
