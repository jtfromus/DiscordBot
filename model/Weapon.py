class Weapon:
    def __init__(self, name, url, weapon_type, rarity):
        self.name = name
        self.url = url
        self.weapon_type = weapon_type
        self.rarity = rarity

    def get_name(self) -> str:
        return self.name

    def get_url(self) -> str:
        return self.url

    def get_weapon_type(self) -> str:
        return self.weapon_type

    def get_rarity(self) -> str:
        return self.rarity

    def set_name(self, name: str) -> None:
        self.name = name

    def set_url(self, url: str) -> None:
        self.url = url

    def set_weapon_type(self, weapon_type: str) -> None:
        self.weapon_type = weapon_type

    def set_rarity(self, rarity: str) -> None:
        self.rarity = rarity
