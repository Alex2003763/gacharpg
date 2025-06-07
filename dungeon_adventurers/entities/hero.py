from dungeon_adventurers.game_data.game_enums import Profession, Rarity, Element, ItemType
# We'll need Item later for the inventory, so keep the import if it was there.

class Hero:
    """
    Represents a hero in the game.
    """
    def __init__(self,
                 name: str,
                 rarity: Rarity,
                 profession: Profession,
                 element: Element,
                 level: int = 1):
        self.name = name
        self.rarity = rarity
        self.profession = profession
        self.element = element
        self.level = level
        self.star_level = 1

        # Base Stats
        self.base_stats = {
            "HP": 100,
            "Attack": 10,
            "Defense": 5,
            "Speed": 10
        }

        # Advanced Stats
        self.advanced_stats = {
            "CritRate": 0.05,      # 5%
            "CritDamage": 1.5,     # 150%
            "HitChance": 1.0,      # 100%
            "Evasion": 0.05,       # 5%
            "EffectResistance": 0.0
        }

        # Skill placeholders
        self.active_skill = None # Will be defined later
        self.passive_skill = None # Will be defined later
        self.leader_skill = None # Will be defined later

        self.inventory = [] # Keeping existing inventory

    # Keeping existing inventory methods
    def add_item(self, item: 'Item'): # Forward reference for Item type
        """
        Adds an item to the hero's inventory.
        """
        self.inventory.append(item)

    def remove_item(self, item_name: str):
        """
        Removes an item from the hero's inventory by its name.
        Returns True if the item was removed, False otherwise.
        """
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return True
        return False

    def get_inventory_details(self) -> str:
        """
        Returns a string detailing the hero's inventory.
        """
        if not self.inventory:
            return f"{self.name}'s inventory is empty."
        details = f"{self.name}'s Inventory:\n"
        # Requires Item class to have name and item_type.value
        # For now, this might cause an error if Item is not fully defined
        # or if item objects don't have these attributes.
        # We'll assume Item will be compatible.
        for item in self.inventory:
            try:
                details += f"- {item.name} ({item.item_type.value})\n"
            except AttributeError:
                details += f"- {item.name} (Unknown type)\n"

        return details

    def __str__(self) -> str:
        return (f"Hero: {self.name} (Lvl: {self.level}, {self.rarity.name} {self.profession.value}, Element: {self.element.value})\n"
                f"  Base Stats: {self.base_stats}\n"
                f"  Advanced Stats: {self.advanced_stats}")
