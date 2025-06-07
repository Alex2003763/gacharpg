from enum import Enum, auto

class Rarity(Enum):
    """
    Represents the rarity of a hero or item.
    """
    N = auto()
    R = auto()
    SR = auto()
    SSR = auto()
    UR = auto()

class Profession(Enum):
    """
    Represents the profession or class of a hero.
    """
    WARRIOR = "Warrior"
    MAGE = "Mage"
    SUPPORT = "Support"
    TANK = "Tank"
    ASSASSIN = "Assassin" # Changed from Rogue, added others

class Element(Enum):
    """
    Represents the elemental affinity.
    """
    WATER = "Water"
    FIRE = "Fire"
    GRASS = "Grass"
    LIGHT = "Light"
    DARK = "Dark"

class ItemType(Enum):
    """
    Represents the type of an item.
    (Keeping this existing enum as it might be useful later)
    """
    WEAPON = "Weapon"
    ARMOR = "Armor"
    POTION = "Potion"

class EquipmentSlot(Enum):
    """
    Represents the slot where an equipment can be fitted.
    """
    WEAPON = auto()
    HELMET = auto()
    CHEST_ARMOR = auto()
    SHOES = auto()
    ACCESSORY = auto()

class ItemQuality(Enum):
    """
    Represents the quality or grade of an item/equipment.
    """
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()
