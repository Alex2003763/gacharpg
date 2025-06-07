from dungeon_adventurers.entities.hero import Hero
from dungeon_adventurers.entities.item import Item
from dungeon_adventurers.game_data.game_enums import HeroClass, ItemType

def main():
    """
    Main function to demonstrate the Dungeon Adventurers classes.
    """
    # Create a Warrior hero
    warrior_hero = Hero(name="Aragorn", hero_class=HeroClass.WARRIOR)
    print(warrior_hero)

    # Create some items
    sword = Item(name="Dragon Slayer", item_type=ItemType.WEAPON, effect_value=25)
    shield = Item(name="Iron Shield", item_type=ItemType.ARMOR, effect_value=15)
    health_potion = Item(name="Minor Health Potion", item_type=ItemType.POTION, effect_value=20)

    print(sword)
    print(shield)
    print(health_potion)

    # Add items to hero's inventory
    warrior_hero.add_item(sword)
    warrior_hero.add_item(shield)
    warrior_hero.add_item(health_potion)

    # Display hero's inventory
    print(warrior_hero.get_inventory_details())

    # Remove an item and display inventory again
    warrior_hero.remove_item("Iron Shield")
    print(warrior_hero.get_inventory_details())

    # Create a Mage hero and display details
    mage_hero = Hero(name="Gandalf", hero_class=HeroClass.MAGE)
    print(mage_hero)
    staff = Item(name="Staff of Power", item_type=ItemType.WEAPON, effect_value=30)
    mage_hero.add_item(staff)
    print(mage_hero.get_inventory_details())

if __name__ == "__main__":
    main()
