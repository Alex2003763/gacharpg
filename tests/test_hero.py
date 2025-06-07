import unittest
from dungeon_adventurers.entities.hero import Hero
from dungeon_adventurers.entities.equipment import Equipment
from dungeon_adventurers.entities.item import Item
from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element, ItemType, EquipmentSlot, ItemQuality

class TestHero(unittest.TestCase):

    # --- Existing tests from previous subtasks ---
    def test_hero_creation_defaults(self):
        hero = Hero(name="TestHero",
                    rarity=Rarity.N,
                    profession=Profession.WARRIOR,
                    element=Element.FIRE)
        self.assertEqual(hero.name, "TestHero")
        self.assertEqual(hero.rarity, Rarity.N)
        self.assertEqual(hero.profession, Profession.WARRIOR)
        self.assertEqual(hero.element, Element.FIRE)
        self.assertEqual(hero.level, 1)
        self.assertEqual(hero.star_level, 1)
        self.assertIsInstance(hero.base_stats, dict)
        self.assertIn("HP", hero.base_stats)
        self.assertIsInstance(hero.advanced_stats, dict)
        self.assertIn("CritRate", hero.advanced_stats)
        self.assertIsNone(hero.active_skill)

    def test_hero_creation_with_level(self):
        hero = Hero(name="HighLevelHero",
                    rarity=Rarity.SSR,
                    profession=Profession.MAGE,
                    element=Element.WATER,
                    level=50)
        self.assertEqual(hero.level, 50)

    def test_hero_base_stats_initial_values(self):
        hero = Hero(name="StatCheckHero", rarity=Rarity.R, profession=Profession.TANK, element=Element.GRASS)
        self.assertEqual(hero.base_stats["HP"], 100)
        self.assertEqual(hero.base_stats["Attack"], 10)

    def test_hero_advanced_stats_initial_values(self):
        hero = Hero(name="AdvStatCheckHero", rarity=Rarity.SR, profession=Profession.ASSASSIN, element=Element.DARK)
        self.assertEqual(hero.advanced_stats["CritRate"], 0.05)
        self.assertEqual(hero.advanced_stats["CritDamage"], 1.5)

    # --- New setUp and tests for equipment ---
    def setUp(self):
        # Re-initialize hero for each test method to ensure independence
        self.hero = Hero(name="TestHero",
                         rarity=Rarity.N,
                         profession=Profession.WARRIOR,
                         element=Element.FIRE)

        # Sample equipment
        self.sword = Equipment(name="Basic Sword",
                               description="A simple sword.",
                               slot=EquipmentSlot.WEAPON,
                               quality=ItemQuality.COMMON,
                               main_stat={"stat_type": "Attack", "value": 10})

        self.helmet = Equipment(name="Leather Cap",
                                description="A basic cap.",
                                slot=EquipmentSlot.HELMET,
                                quality=ItemQuality.COMMON,
                                main_stat={"stat_type": "Defense", "value": 5})

        self.another_sword = Equipment(name="Sharp Sword",
                               description="A sharper sword.",
                               slot=EquipmentSlot.WEAPON,
                               quality=ItemQuality.UNCOMMON,
                               main_stat={"stat_type": "Attack", "value": 15})

    def test_equip_item_valid(self):
        # Equip a sword
        returned_item = self.hero.equip_item(self.sword)
        self.assertIsNone(returned_item, "No item should be returned when equipping to an empty slot.")
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.sword)
        self.assertIn(self.sword.name, self.hero.get_equipment_details())

        # Equip a helmet
        returned_item_helmet = self.hero.equip_item(self.helmet)
        self.assertIsNone(returned_item_helmet)
        self.assertEqual(self.hero.equipment[EquipmentSlot.HELMET], self.helmet)
        self.assertIn(self.helmet.name, self.hero.get_equipment_details())

    def test_equip_item_replace_existing(self):
        # Equip first sword
        self.hero.equip_item(self.sword)
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.sword)

        # Equip another sword in the same slot
        returned_item = self.hero.equip_item(self.another_sword)
        self.assertEqual(returned_item, self.sword, "The previously equipped sword should be returned.")
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.another_sword, "The new sword should now be equipped.")
        self.assertIn(self.another_sword.name, self.hero.get_equipment_details())
        self.assertNotIn(self.sword.name, self.hero.get_equipment_details())

    def test_equip_item_invalid_type(self):
        # Create a non-equipment item (using Item base class)
        potion = Item(name="Health Potion", item_type=ItemType.POTION, description="Heals HP.")
        with self.assertRaisesRegex(ValueError, "Item is not a piece of equipment."):
            self.hero.equip_item(potion)

    def test_unequip_item_valid(self):
        # Equip an item first
        self.hero.equip_item(self.sword)
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.sword)

        # Unequip the item
        unequipped_item = self.hero.unequip_item(EquipmentSlot.WEAPON)
        self.assertEqual(unequipped_item, self.sword, "The unequipped item should be the sword.")
        self.assertIsNone(self.hero.equipment[EquipmentSlot.WEAPON], "The weapon slot should now be empty.")
        self.assertNotIn(self.sword.name, self.hero.get_equipment_details())
        if not any(self.hero.equipment.values()): # Check if all equipment slots are None
             self.assertEqual(self.hero.get_equipment_details(), f"{self.hero.name} has no equipment.")

    def test_unequip_item_empty_slot(self):
        unequipped_item = self.hero.unequip_item(EquipmentSlot.WEAPON)
        self.assertIsNone(unequipped_item, "Nothing should be returned from an empty slot.")
        self.assertIsNone(self.hero.equipment[EquipmentSlot.WEAPON])

    def test_unequip_item_invalid_slot_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid slot specified for unequipping."):
            self.hero.unequip_item("NOT_A_SLOT") # Pass a string instead of EquipmentSlot enum

if __name__ == '__main__':
    unittest.main()
