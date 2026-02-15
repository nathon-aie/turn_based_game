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

    # แปลงเป็น Dictionary เพื่อเตรียมเซฟ
    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "atk": self.atk,
            "atk_buff": self.atk_buff,
        }

    # รับข้อมูล Dictionary มาแปลงสำหรับโหลด
    def load_from_dict(self, data):
        self.name = data.get("name", self.name)
        self.hp = data.get("hp", self.hp)
        self.max_hp = data.get("max_hp", self.max_hp)
        self.atk = data.get("atk", self.atk)
        self.atk_buff = data.get("atk_buff", 1)
