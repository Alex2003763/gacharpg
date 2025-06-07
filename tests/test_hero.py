import unittest
from dungeon_adventurers.entities.hero import Hero
from dungeon_adventurers.entities.equipment import Equipment
from dungeon_adventurers.entities.item import Item
from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element, ItemType, EquipmentSlot, ItemQuality, SkillTargetType # Added SkillTargetType
from dungeon_adventurers.entities.skills import ActiveSkill, PassiveSkill, LeaderSkill # Added skill classes

class TestHero(unittest.TestCase):

    # --- Existing tests from previous subtasks (summarized for brevity in thought process) ---
    def test_hero_creation_defaults(self):
        hero = Hero(name="TestHeroDefaults", rarity=Rarity.N, profession=Profession.WARRIOR, element=Element.FIRE)
        self.assertEqual(hero.name, "TestHeroDefaults")
        self.assertEqual(hero.level, 1)
        self.assertIsNone(hero.active_skill) # Check initial skill state
        self.assertIsNone(hero.passive_skill)
        self.assertIsNone(hero.leader_skill)

    def test_hero_creation_with_level(self):
        hero = Hero(name="HighLevelHero", rarity=Rarity.SSR, profession=Profession.MAGE, element=Element.WATER, level=50)
        self.assertEqual(hero.level, 50)

    def test_hero_base_stats_initial_values(self):
        hero = Hero(name="StatCheckHero", rarity=Rarity.R, profession=Profession.TANK, element=Element.GRASS)
        self.assertEqual(hero.base_stats["HP"], 100)

    def test_hero_advanced_stats_initial_values(self):
        hero = Hero(name="AdvStatCheckHero", rarity=Rarity.SR, profession=Profession.ASSASSIN, element=Element.DARK)
        self.assertEqual(hero.advanced_stats["CritRate"], 0.05)

    # --- Updated setUp to include skills ---
    def setUp(self):
        # Initialize hero
        self.hero = Hero(name="TestHero",
                         rarity=Rarity.N,
                         profession=Profession.WARRIOR,
                         element=Element.FIRE)

        # Sample equipment
        self.sword = Equipment(name="Basic Sword", description="A simple sword.", slot=EquipmentSlot.WEAPON,
                               quality=ItemQuality.COMMON, main_stat={"stat_type": "Attack", "value": 10})
        self.helmet = Equipment(name="Leather Cap", description="A basic cap.", slot=EquipmentSlot.HELMET,
                                quality=ItemQuality.COMMON, main_stat={"stat_type": "Defense", "value": 5})
        self.another_sword = Equipment(name="Sharp Sword", description="A sharper sword.", slot=EquipmentSlot.WEAPON,
                                       quality=ItemQuality.UNCOMMON, main_stat={"stat_type": "Attack", "value": 15})

        # Sample skills
        self.sample_active_skill = ActiveSkill(name="Slash", description="A basic attack.",
                                               target_type=SkillTargetType.ENEMY_SINGLE,
                                               effects=[{"effect_type": "damage", "value": 100}])
        self.sample_passive_skill = PassiveSkill(name="Fortitude", description="Increases HP.",
                                                 target_type=SkillTargetType.SELF,
                                                 effects=[{"effect_type": "stat_mod", "stat": "HP", "percentage": 0.1}])
        self.sample_leader_skill = LeaderSkill(name="Team Attack Boost", description="Boosts team attack.",
                                               effects=[{"effect_type": "stat_mod", "stat": "Attack", "percentage": 0.05}],
                                               target_type=SkillTargetType.ALLY_TEAM) # Explicitly set for clarity, though it's default
        self.another_active_skill = ActiveSkill(name="Fireball", description="Shoots a fireball.",
                                               target_type=SkillTargetType.ENEMY_SINGLE,
                                               effects=[{"effect_type": "damage", "value": 150, "element": Element.FIRE}])

    # --- Existing Equipment tests (summarized) ---
    def test_equip_item_valid(self):
        returned_item = self.hero.equip_item(self.sword)
        self.assertIsNone(returned_item)
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.sword)

    def test_equip_item_replace_existing(self):
        self.hero.equip_item(self.sword)
        returned_item = self.hero.equip_item(self.another_sword)
        self.assertEqual(returned_item, self.sword)
        self.assertEqual(self.hero.equipment[EquipmentSlot.WEAPON], self.another_sword)

    def test_equip_item_invalid_type(self):
        potion = Item(name="Health Potion", item_type=ItemType.POTION, description="Heals HP.")
        with self.assertRaisesRegex(ValueError, "Item is not a piece of equipment."):
            self.hero.equip_item(potion)

    def test_unequip_item_valid(self):
        self.hero.equip_item(self.sword)
        unequipped_item = self.hero.unequip_item(EquipmentSlot.WEAPON)
        self.assertEqual(unequipped_item, self.sword)
        self.assertIsNone(self.hero.equipment[EquipmentSlot.WEAPON])

    def test_unequip_item_empty_slot(self):
        unequipped_item = self.hero.unequip_item(EquipmentSlot.WEAPON)
        self.assertIsNone(unequipped_item)

    def test_unequip_item_invalid_slot_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid slot specified for unequipping."):
            self.hero.unequip_item("NOT_A_SLOT")

    # --- New Skill Assignment Tests ---
    def test_set_active_skill_valid(self):
        self.hero.set_active_skill(self.sample_active_skill)
        self.assertEqual(self.hero.active_skill, self.sample_active_skill)
        self.assertEqual(self.hero.active_skill.name, "Slash")
        self.assertIn("Active: Slash", self.hero.get_skills_details())

    def test_set_active_skill_none(self):
        self.hero.set_active_skill(self.sample_active_skill) # Assign one first
        self.hero.set_active_skill(None) # Then set to None
        self.assertIsNone(self.hero.active_skill)
        self.assertIn("Active: None", self.hero.get_skills_details())

    def test_set_active_skill_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Assigned skill must be an ActiveSkill instance or None."):
            self.hero.set_active_skill(self.sample_passive_skill) # Try to assign a PassiveSkill

    def test_set_passive_skill_valid(self):
        self.hero.set_passive_skill(self.sample_passive_skill)
        self.assertEqual(self.hero.passive_skill, self.sample_passive_skill)
        self.assertEqual(self.hero.passive_skill.name, "Fortitude")
        self.assertIn("Passive: Fortitude", self.hero.get_skills_details())

    def test_set_passive_skill_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Assigned skill must be a PassiveSkill instance or None."):
            self.hero.set_passive_skill(self.sample_active_skill)

    def test_set_leader_skill_valid(self):
        self.hero.set_leader_skill(self.sample_leader_skill)
        self.assertEqual(self.hero.leader_skill, self.sample_leader_skill)
        self.assertEqual(self.hero.leader_skill.name, "Team Attack Boost")
        self.assertIn("Leader: Team Attack Boost", self.hero.get_skills_details())

    def test_set_leader_skill_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Assigned skill must be a LeaderSkill instance or None."):
            self.hero.set_leader_skill(self.sample_active_skill)

    def test_hero_str_includes_skills(self):
        self.hero.set_active_skill(self.sample_active_skill)
        self.hero.set_passive_skill(self.sample_passive_skill)
        hero_str = str(self.hero)
        self.assertIn("Active: Slash", hero_str)
        self.assertIn("Passive: Fortitude", hero_str)
        self.assertIn("Leader: None", hero_str) # Leader skill not set by default in setUp

if __name__ == '__main__':
    unittest.main()
