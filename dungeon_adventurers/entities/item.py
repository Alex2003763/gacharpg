from dungeon_adventurers.game_data.game_enums import ItemType

class Item:
    """
    Represents a generic item in the game.
    This class is intended to be a base for more specific item types.
    """
    def __init__(self, name: str, item_type: ItemType, description: str = ""):
        self.name = name
        self.item_type = item_type
        self.description = description

    def __str__(self) -> str:
        return f"Item: {self.name} (Type: {self.item_type.value})"
