from dungeon_adventurers.game_data.game_enums import Profession, Rarity, Element, ItemType, EquipmentSlot
from dungeon_adventurers.entities.equipment import Equipment # Added import

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

        self.base_stats = {
            "HP": 100, "Attack": 10, "Defense": 5, "Speed": 10
        }
        self.advanced_stats = {
            "CritRate": 0.05, "CritDamage": 1.5, "HitChance": 1.0,
            "Evasion": 0.05, "EffectResistance": 0.0
        }

        self.active_skill = None
        self.passive_skill = None
        self.leader_skill = None

        self.inventory = []

        # Equipment slots, initialized to None
        self.equipment = {slot: None for slot in EquipmentSlot} # Added

    def equip_item(self, item_to_equip: Equipment) -> Equipment | None:
        """
        Equips an item to the appropriate slot.
        Returns the previously equipped item in that slot, if any.
        Raises ValueError if the item is not an Equipment instance or slot is invalid.
        """
        if not isinstance(item_to_equip, Equipment):
            raise ValueError("Item is not a piece of equipment.")

        slot_to_equip_in = item_to_equip.slot
        if not isinstance(slot_to_equip_in, EquipmentSlot):
            # This should not happen if Equipment class ensures slot is EquipmentSlot type
            raise ValueError("Invalid equipment slot type on the item.")

        # Check if the slot exists in hero's equipment (it should, due to init)
        if slot_to_equip_in not in self.equipment:
            raise ValueError(f"Hero does not have a slot: {slot_to_equip_in.name}")

        previously_equipped_item = self.equipment[slot_to_equip_in]
        self.equipment[slot_to_equip_in] = item_to_equip
        # print(f"{self.name} equipped {item_to_equip.name} in {slot_to_equip_in.name}.")
        return previously_equipped_item

    def unequip_item(self, slot_to_unequip: EquipmentSlot) -> Equipment | None:
        """
        Unequips an item from the specified slot.
        Returns the unequipped item, or None if the slot was empty.
        Raises ValueError if the slot is invalid.
        """
        if not isinstance(slot_to_unequip, EquipmentSlot):
            raise ValueError("Invalid slot specified for unequipping.")

        if slot_to_unequip not in self.equipment:
            # Should not happen if self.equipment is initialized with all EquipmentSlots
            raise ValueError(f"Hero does not have a slot: {slot_to_unequip.name}")

        equipped_item = self.equipment[slot_to_unequip]
        if equipped_item:
            self.equipment[slot_to_unequip] = None
            # print(f"{self.name} unequipped {equipped_item.name} from {slot_to_unequip.name}.")
        return equipped_item

    # --- Existing inventory methods (assuming they handle non-equipment items) ---
    def add_item(self, item): # General item, not necessarily Equipment
        """Adds an item to the hero's general inventory."""
        self.inventory.append(item)

    def remove_item(self, item_name: str):
        """Removes an item from the hero's general inventory by name."""
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return True
        return False

    def get_inventory_details(self) -> str:
        if not self.inventory:
            return f"{self.name}'s inventory is empty."
        details = f"{self.name}'s Inventory (non-equipped):\n"
        for item in self.inventory:
            try:
                details += f"- {item.name} ({item.item_type.value})\n"
            except AttributeError:
                details += f"- {item.name} (Unknown type)\n"
        return details

    def get_equipment_details(self) -> str:
        details = f"{self.name}'s Equipment:\n"
        equipped_count = 0
        for slot, item in self.equipment.items():
            if item:
                details += f"  {slot.name}: {item.name} ({item.quality.name} {item.item_type.name})\n"
                equipped_count +=1
            else:
                details += f"  {slot.name}: Empty\n"
        if equipped_count == 0:
            return f"{self.name} has no equipment."
        return details


    def __str__(self) -> str:
        return (f"Hero: {self.name} (Lvl: {self.level}, {self.rarity.name} {self.profession.value}, Element: {self.element.value})\n"
                f"  Base Stats: {self.base_stats}\n"
                f"  Advanced Stats: {self.advanced_stats}\n"
                f"{self.get_equipment_details()}\n"
                f"{self.get_inventory_details()}")
