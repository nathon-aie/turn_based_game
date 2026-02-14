import gamedata


class Enemy:
    def __init__(self, name):
        data = gamedata.ENEMIES.get(name, {})
        self.name = name
        self.hp = data.get("hp", 50)
        self.max_hp = self.hp
        self.atk = data.get("atk", 5)
        self.atk_buff = 1
        self.skills = data.get("skills", [])
