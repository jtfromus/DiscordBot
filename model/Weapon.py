class Weapon:
    def __init__(self, hash: int, name: str, screen_shot: str, icon: str, weapon_type: str, rarity: str, perks: {}) -> None:
        self.hash = hash
        self.name = name
        self.screen_shot = screen_shot
        self.icon = icon
        self.weapon_type = weapon_type
        self.rarity = rarity
        self.perks = perks

    def get_hash(self) -> int:
        return self.hash

    def get_name(self) -> str:
        return self.name

    def get_screen_shot(self) -> str:
        return self.screen_shot

    def get_icon(self) -> str:
        return self.icon

    def get_weapon_type(self) -> str:
        return self.weapon_type

    def get_rarity(self) -> str:
        return self.rarity

    def get_perks(self) -> {}:
        return self.perks

    def set_hash(self, hash: int) -> None:
        self.hash = hash

    def set_name(self, name: str) -> None:
        self.name = name

    def set_screen_shot(self, screen_shot: str) -> None:
        self.screen_shot = screen_shot

    def set_icon(self, icon: str) -> None:
        self.icon = icon

    def set_weapon_type(self, weapon_type: str) -> None:
        self.weapon_type = weapon_type

    def set_rarity(self, rarity: str) -> None:
        self.rarity = rarity

    def set_perks(self, perks: {}) -> None:
        self.perks = perks


# This function will find the weapon obj in the given list
def find_weapon(weapons: [], name: str) -> Weapon:
    for weapon in weapons:
        if weapon.get_name().lower() == name.lower():
            return weapon
    return None
