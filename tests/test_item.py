import unittest
from dungeon_adventurers.entities.item import Item
from dungeon_adventurers.game_data.game_enums import ItemType

class TestItem(unittest.TestCase):

    def test_item_creation_all_fields(self):
        item = Item(name="Health Potion",
                    item_type=ItemType.POTION,
                    description="Restores a small amount of health.")
        self.assertEqual(item.name, "Health Potion")
        self.assertEqual(item.item_type, ItemType.POTION)
        self.assertEqual(item.description, "Restores a small amount of health.")

    def test_item_creation_default_description(self):
        item = Item(name="Mysterious Scroll",
                    item_type=ItemType.WEAPON) # Using WEAPON just for enum variety
        self.assertEqual(item.name, "Mysterious Scroll")
        self.assertEqual(item.item_type, ItemType.WEAPON)
        self.assertEqual(item.description, "", "Description should default to an empty string.")

    def test_item_str_representation(self):
        item = Item(name="Mana Potion",
                    item_type=ItemType.POTION,
                    description="Restores mana.")
        expected_str = f"Item: Mana Potion (Type: {ItemType.POTION.value})" # Use .value for consistency
        self.assertEqual(str(item), expected_str)

if __name__ == '__main__':
    unittest.main()
