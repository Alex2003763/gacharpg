import unittest
from dungeon_adventurers.entities.equipment import Equipment
from dungeon_adventurers.entities.item import Item # To check inheritance
from dungeon_adventurers.game_data.game_enums import ItemType, EquipmentSlot, ItemQuality

class TestEquipment(unittest.TestCase):

    def test_equipment_creation_all_fields(self):
        main_stat = {"stat_type": "Attack", "value": 50}
        sub_stats = [{"stat_type": "HP", "value": 100}, {"stat_type": "CritRate", "value": 0.05}]

        sword = Equipment(name="Excalibur",
                          description="A legendary sword.",
                          slot=EquipmentSlot.WEAPON,
                          quality=ItemQuality.LEGENDARY,
                          main_stat=main_stat,
                          sub_stats=sub_stats,
                          set_name="King's Set")

        self.assertIsInstance(sword, Item) # Check inheritance
        self.assertEqual(sword.name, "Excalibur")
        self.assertEqual(sword.description, "A legendary sword.")
        self.assertEqual(sword.item_type, ItemType.WEAPON) # Inferred from slot
        self.assertEqual(sword.slot, EquipmentSlot.WEAPON)
        self.assertEqual(sword.quality, ItemQuality.LEGENDARY)
        self.assertEqual(sword.main_stat, main_stat)
        self.assertEqual(sword.sub_stats, sub_stats)
        self.assertEqual(sword.set_name, "King's Set")

    def test_equipment_creation_defaults(self):
        main_stat = {"stat_type": "Defense", "value": 30}
        helmet = Equipment(name="Iron Helm",
                           description="A sturdy helmet.",
                           slot=EquipmentSlot.HELMET,
                           quality=ItemQuality.COMMON,
                           main_stat=main_stat)

        self.assertEqual(helmet.item_type, ItemType.ARMOR) # Inferred from slot
        self.assertEqual(helmet.sub_stats, []) # Default empty list
        self.assertIsNone(helmet.set_name) # Default None

    def test_equipment_item_type_inference(self):
        weapon = Equipment("Axe", "A basic axe", EquipmentSlot.WEAPON, ItemQuality.COMMON, {"stat_type": "Attack", "value": 10})
        self.assertEqual(weapon.item_type, ItemType.WEAPON)

        helmet = Equipment("Leather Cap", "A simple cap", EquipmentSlot.HELMET, ItemQuality.COMMON, {"stat_type": "Defense", "value": 5})
        self.assertEqual(helmet.item_type, ItemType.ARMOR)

        chest = Equipment("Chainmail", "Provides good protection", EquipmentSlot.CHEST_ARMOR, ItemQuality.UNCOMMON, {"stat_type": "Defense", "value": 20})
        self.assertEqual(chest.item_type, ItemType.ARMOR)

        shoes = Equipment("Boots", "Standard issue boots", EquipmentSlot.SHOES, ItemQuality.COMMON, {"stat_type": "Speed", "value": 5})
        self.assertEqual(shoes.item_type, ItemType.ARMOR)

        accessory = Equipment("Ring of Power", "A mysterious ring", EquipmentSlot.ACCESSORY, ItemQuality.RARE, {"stat_type": "HP", "value": 50})
        self.assertEqual(accessory.item_type, ItemType.ARMOR) # Currently defaults to ARMOR

    def test_equipment_str_representation(self):
        main_stat = {"stat_type": "Attack", "value": 50}
        sword = Equipment(name="Excalibur",
                          description="A legendary sword.",
                          slot=EquipmentSlot.WEAPON,
                          quality=ItemQuality.LEGENDARY,
                          main_stat=main_stat,
                          sub_stats=[{"stat_type": "HP", "value": 100}],
                          set_name="King's Set")

        # Based on Equipment.__str__
        # Example: Equipment: Excalibur (Slot: WEAPON, Quality: LEGENDARY, Type: WEAPON)
        # We will check for key components in the string
        output_str = str(sword)
        self.assertIn("Equipment: Excalibur", output_str)
        self.assertIn("Slot: WEAPON", output_str)
        self.assertIn("Quality: LEGENDARY", output_str)
        self.assertIn("Type: WEAPON", output_str) # Check item_type name
        self.assertIn("Main Stat: Attack: 50", output_str)
        self.assertIn("Sub Stats: HP: 100", output_str)
        self.assertIn("Set: King's Set", output_str)

if __name__ == '__main__':
    unittest.main()
