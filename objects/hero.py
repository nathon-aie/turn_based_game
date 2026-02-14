import gamedata


class Hero:
    def __init__(self, name):
        data = gamedata.HEROES.get(name, {})
        self.name = name
        self.hp = data.get("hp", 100)
        self.max_hp = self.hp
        self.atk = data.get("atk", 10)
        self.atk_buff = 1
        self.skills = data.get("skills", [])
