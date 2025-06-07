from dungeon_adventurers.game_data.game_enums import Profession, Rarity, Element, ItemType, EquipmentSlot
from dungeon_adventurers.entities.equipment import Equipment
# Added imports for skills:
from dungeon_adventurers.entities.skills import Skill, ActiveSkill, PassiveSkill, LeaderSkill # Assuming base Skill might be useful for type hints somewhere
from dungeon_adventurers.game_data.game_enums import SkillType # If needed for logic, though skill instances carry their type

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

        self.inventory = []
        self.equipment = {slot: None for slot in EquipmentSlot}

        # Initialize skill slots to None
        self.active_skill: ActiveSkill | None = None
        self.passive_skill: PassiveSkill | None = None
        self.leader_skill: LeaderSkill | None = None

    # --- Skill setter methods ---
    def set_active_skill(self, skill: ActiveSkill | None):
        if skill is not None and not isinstance(skill, ActiveSkill):
            raise TypeError("Assigned skill must be an ActiveSkill instance or None.")
        self.active_skill = skill

    def set_passive_skill(self, skill: PassiveSkill | None):
        # GDD implies multiple passive skills are possible. For now, one.
        # If multiple, this would be add_passive_skill and self.passive_skills would be a list.
        if skill is not None and not isinstance(skill, PassiveSkill):
            raise TypeError("Assigned skill must be a PassiveSkill instance or None.")
        self.passive_skill = skill

    def set_leader_skill(self, skill: LeaderSkill | None):
        if skill is not None and not isinstance(skill, LeaderSkill):
            raise TypeError("Assigned skill must be a LeaderSkill instance or None.")
        self.leader_skill = skill

    # --- Existing Equipment methods ---
    def equip_item(self, item_to_equip: Equipment) -> Equipment | None:
        if not isinstance(item_to_equip, Equipment):
            raise ValueError("Item is not a piece of equipment.")
        slot_to_equip_in = item_to_equip.slot
        if not isinstance(slot_to_equip_in, EquipmentSlot):
            raise ValueError("Invalid equipment slot type on the item.")
        if slot_to_equip_in not in self.equipment:
            raise ValueError(f"Hero does not have a slot: {slot_to_equip_in.name}")
        previously_equipped_item = self.equipment[slot_to_equip_in]
        self.equipment[slot_to_equip_in] = item_to_equip
        return previously_equipped_item

    def unequip_item(self, slot_to_unequip: EquipmentSlot) -> Equipment | None:
        if not isinstance(slot_to_unequip, EquipmentSlot):
            raise ValueError("Invalid slot specified for unequipping.")
        if slot_to_unequip not in self.equipment:
            raise ValueError(f"Hero does not have a slot: {slot_to_unequip.name}")
        equipped_item = self.equipment[slot_to_unequip]
        if equipped_item:
            self.equipment[slot_to_unequip] = None
        return equipped_item

    # --- Existing Inventory methods ---
    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item_name: str):
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

    def get_skills_details(self) -> str:
        details = f"{self.name}'s Skills:\n"
        skills_count = 0
        if self.active_skill:
            details += f"  Active: {self.active_skill.name} - {self.active_skill.description}\n"
            skills_count +=1
        else:
            details += "  Active: None\n"
        if self.passive_skill:
            details += f"  Passive: {self.passive_skill.name} - {self.passive_skill.description}\n"
            skills_count +=1
        else:
            details += "  Passive: None\n"
        if self.leader_skill:
            details += f"  Leader: {self.leader_skill.name} - {self.leader_skill.description}\n"
            skills_count +=1
        else:
            details += "  Leader: None\n"
        if skills_count == 0:
            # This part might be redundant if we always list the slots.
            # For consistency with get_equipment_details, let's keep it simple.
            pass
        return details

    def __str__(self) -> str:
        # Basic info
        info_str = (f"Hero: {self.name} (Lvl: {self.level}, {self.rarity.name} {self.profession.value}, Element: {self.element.value})\n"
                    f"  Base Stats: {self.base_stats}\n"
                    f"  Advanced Stats: {self.advanced_stats}")

        # Equipment details
        equipment_str = self.get_equipment_details()

        # Skills details
        skills_str = self.get_skills_details()

        # Inventory details
        inventory_str = self.get_inventory_details()

        return f"{info_str}\n{equipment_str}\n{skills_str}\n{inventory_str}"
