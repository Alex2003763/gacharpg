import unittest
from dungeon_adventurers.entities.hero import Hero
from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element

class TestHero(unittest.TestCase):

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

        # Check base stats structure and keys
        self.assertIsInstance(hero.base_stats, dict)
        self.assertIn("HP", hero.base_stats)
        self.assertIn("Attack", hero.base_stats)
        self.assertIn("Defense", hero.base_stats)
        self.assertIn("Speed", hero.base_stats)

        # Check advanced stats structure and keys
        self.assertIsInstance(hero.advanced_stats, dict)
        self.assertIn("CritRate", hero.advanced_stats)
        self.assertIn("CritDamage", hero.advanced_stats)
        self.assertIn("HitChance", hero.advanced_stats)
        self.assertIn("Evasion", hero.advanced_stats)
        self.assertIn("EffectResistance", hero.advanced_stats)

        # Check skill placeholders
        self.assertIsNone(hero.active_skill)
        self.assertIsNone(hero.passive_skill)
        self.assertIsNone(hero.leader_skill)

    def test_hero_creation_with_level(self):
        hero = Hero(name="HighLevelHero",
                    rarity=Rarity.SSR,
                    profession=Profession.MAGE,
                    element=Element.WATER,
                    level=50)
        self.assertEqual(hero.name, "HighLevelHero")
        self.assertEqual(hero.rarity, Rarity.SSR)
        self.assertEqual(hero.profession, Profession.MAGE)
        self.assertEqual(hero.element, Element.WATER)
        self.assertEqual(hero.level, 50)

    def test_hero_base_stats_initial_values(self):
        # This test assumes specific default values.
        # These might change if we implement stat calculation based on rarity/level later.
        hero = Hero(name="StatCheckHero", rarity=Rarity.R, profession=Profession.TANK, element=Element.GRASS)
        self.assertEqual(hero.base_stats["HP"], 100)
        self.assertEqual(hero.base_stats["Attack"], 10)
        self.assertEqual(hero.base_stats["Defense"], 5)
        self.assertEqual(hero.base_stats["Speed"], 10)

    def test_hero_advanced_stats_initial_values(self):
        hero = Hero(name="AdvStatCheckHero", rarity=Rarity.SR, profession=Profession.ASSASSIN, element=Element.DARK)
        self.assertEqual(hero.advanced_stats["CritRate"], 0.05)
        self.assertEqual(hero.advanced_stats["CritDamage"], 1.5)
        self.assertEqual(hero.advanced_stats["HitChance"], 1.0)
        self.assertEqual(hero.advanced_stats["Evasion"], 0.05)
        self.assertEqual(hero.advanced_stats["EffectResistance"], 0.0)

if __name__ == '__main__':
    unittest.main()
