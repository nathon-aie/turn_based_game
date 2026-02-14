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
    "Tanker": {"hp": 200, "atk": 5, "skills": ["Punch", "Heal"]},
}

ENEMIES = {
    "Noob Slayer": {"hp": 500, "atk": 10, "skills": ["Punch"]},
    "Goblin Slayer": {"hp": 500, "atk": 15, "skills": ["Fireball", "Slash"]},
    "God Slayer": {"hp": 500, "atk": 20, "skills": ["Nuke"]},
    "Anuthin": {"hp": 1000, "atk": 25, "skills": ["Punch", "Fireball", "Slash"]},
    "Anuthin Slayer": {"hp": 1500, "atk": 30, "skills": ["Nuke"]},
}
