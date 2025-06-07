from dungeon_adventurers.game_data.game_enums import ItemType

class Item:
    """
    Represents an item that a hero can possess.
    """
    def __init__(self, name: str, item_type: ItemType, effect_value: int):
        self.name = name
        self.item_type = item_type
        self.effect_value = effect_value

    def __str__(self) -> str:
        return f"Item: {self.name} (Type: {self.item_type.value}, Effect: {self.effect_value})"
