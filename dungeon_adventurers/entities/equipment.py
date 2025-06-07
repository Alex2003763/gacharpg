from dungeon_adventurers.entities.item import Item
from dungeon_adventurers.game_data.game_enums import ItemType, EquipmentSlot, ItemQuality

class Equipment(Item):
    """
    Represents a piece of equipment that a Hero can wear.
    Inherits from the base Item class.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 slot: EquipmentSlot,
                 quality: ItemQuality,
                 main_stat: dict, # e.g., {"stat_type": "Attack", "value": 50}
                 sub_stats: list = None,  # List of dicts, e.g., [{"stat_type": "HP", "value": 100}]
                 set_name: str = None):   # Name of the equipment set, if any

        # Equipment should have a specific ItemType, e.g., WEAPON, ARMOR.
        # For simplicity, we'll default to a generic "EQUIPMENT" type if not implicitly defined by slot.
        # A more robust way would be to map EquipmentSlot to ItemType.
        # For now, we will require ItemType to be passed if we want it to be specific,
        # or we can try to infer it. Let's make it explicit for now.
        # However, the GDD implies specific equipment types like "Weapon", "Armor" are ItemTypes.
        # Let's try to map EquipmentSlot to a relevant ItemType.

        mapped_item_type = ItemType.ARMOR # Default
        if slot == EquipmentSlot.WEAPON:
            mapped_item_type = ItemType.WEAPON
        # Other slots like HELMET, CHEST_ARMOR, SHOES, ACCESSORY would typically be ItemType.ARMOR
        # or a more granular "Accessory" ItemType if we add it.

        super().__init__(name, item_type=mapped_item_type, description=description)

        self.slot = slot
        self.quality = quality
        self.main_stat = main_stat
        self.sub_stats = sub_stats if sub_stats is not None else []
        self.set_name = set_name

    def __str__(self) -> str:
        sub_stats_str = 'None'
        if self.sub_stats:
            sub_stats_list = [f"{s.get('stat_type', 'N/A')}: {s.get('value', 'N/A')}" for s in self.sub_stats]
            sub_stats_str = ', '.join(sub_stats_list)

        details = (
            f"Equipment: {self.name} (Slot: {self.slot.name}, Quality: {self.quality.name}, Type: {self.item_type.name})\n"
            f"  Description: {self.description}\n"
            f"  Main Stat: {self.main_stat.get('stat_type', 'N/A')}: {self.main_stat.get('value', 'N/A')}\n"
            f"  Sub Stats: {sub_stats_str}\n"
            f"  Set: {self.set_name if self.set_name else 'None'}"
        )
        return details
