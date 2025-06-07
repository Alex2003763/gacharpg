import unittest
from dungeon_adventurers.entities.skills import Skill, ActiveSkill, PassiveSkill, LeaderSkill
from dungeon_adventurers.game_data.game_enums import SkillType, SkillTargetType, Element

class TestSkillClasses(unittest.TestCase):

    def test_base_skill_creation(self):
        effects = [{"effect_type": "damage", "value": 50, "element": Element.FIRE}]
        skill = Skill(name="Fireball",
                      description="Hurls a small fireball.",
                      skill_type=SkillType.ACTIVE, # Base Skill can be any type for generic use
                      target_type=SkillTargetType.ENEMY_SINGLE,
                      effects=effects)
        self.assertEqual(skill.name, "Fireball")
        self.assertEqual(skill.description, "Hurls a small fireball.")
        self.assertEqual(skill.skill_type, SkillType.ACTIVE)
        self.assertEqual(skill.target_type, SkillTargetType.ENEMY_SINGLE)
        self.assertEqual(skill.effects, effects)
        self.assertIn("Fireball", str(skill))
        self.assertIn("Damage for 50 (FIRE element)", skill.get_effects_description()) # Expected capitalized "Damage"

    def test_base_skill_invalid_init(self):
        with self.assertRaises(ValueError): # Empty name
            Skill("", "Desc", SkillType.ACTIVE, SkillTargetType.SELF, [])
        with self.assertRaises(ValueError): # Invalid skill_type
            Skill("Name", "Desc", "NOT_A_SKILL_TYPE", SkillTargetType.SELF, [])

    def test_active_skill_creation(self):
        effects = [{"effect_type": "heal", "percentage": 0.25, "target_stat": "HP"}]
        active_skill = ActiveSkill(name="Minor Heal",
                                   description="Heals a small amount of HP.",
                                   target_type=SkillTargetType.ALLY_SINGLE,
                                   effects=effects,
                                   cooldown=3,
                                   energy_cost=20)
        self.assertEqual(active_skill.name, "Minor Heal")
        self.assertEqual(active_skill.skill_type, SkillType.ACTIVE) # Verifies it's set by subclass
        self.assertEqual(active_skill.target_type, SkillTargetType.ALLY_SINGLE)
        self.assertEqual(active_skill.effects, effects)
        self.assertEqual(active_skill.cooldown, 3)
        self.assertEqual(active_skill.energy_cost, 20)
        self.assertEqual(active_skill.current_cooldown, 0) # Default current_cooldown
        self.assertTrue(active_skill.is_available())
        self.assertIn("Cost: 20 Energy", str(active_skill))
        self.assertIn("Cooldown: 3 turns", str(active_skill))

        active_skill.put_on_cooldown()
        self.assertEqual(active_skill.current_cooldown, 3)
        self.assertFalse(active_skill.is_available())
        active_skill.reduce_cooldown()
        self.assertEqual(active_skill.current_cooldown, 2)
        active_skill.reduce_cooldown(2)
        self.assertEqual(active_skill.current_cooldown, 0)
        self.assertTrue(active_skill.is_available())

    def test_active_skill_invalid_init(self):
        with self.assertRaises(ValueError): # Negative cooldown
            ActiveSkill("Name", "Desc", SkillTargetType.SELF, [], cooldown=-1)
        with self.assertRaises(ValueError): # Negative energy_cost
            ActiveSkill("Name", "Desc", SkillTargetType.SELF, [], energy_cost=-1)

    def test_passive_skill_creation(self):
        effects = [{"effect_type": "stat_buff", "stat": "Attack", "percentage": 0.1}]
        passive_skill = PassiveSkill(name="Attack Up Aura",
                                     description="Slightly boosts attack.",
                                     target_type=SkillTargetType.SELF, # Or ALLY_TEAM for aura
                                     effects=effects)
        self.assertEqual(passive_skill.name, "Attack Up Aura")
        self.assertEqual(passive_skill.skill_type, SkillType.PASSIVE)
        self.assertEqual(passive_skill.target_type, SkillTargetType.SELF)
        self.assertEqual(passive_skill.effects, effects)
        self.assertIn("Type: Passive", str(passive_skill))

    def test_leader_skill_creation(self):
        effects = [{"effect_type": "stat_buff", "stat": "HP", "percentage": 0.15, "element_filter": Element.FIRE}]
        leader_skill = LeaderSkill(name="Fire Team HP Boost",
                                   description="Boosts HP of Fire allies.",
                                   # target_type defaults to ALLY_TEAM
                                   effects=effects)
        self.assertEqual(leader_skill.name, "Fire Team HP Boost")
        self.assertEqual(leader_skill.skill_type, SkillType.LEADER)
        self.assertEqual(leader_skill.target_type, SkillTargetType.ALLY_TEAM) # Check default
        self.assertEqual(leader_skill.effects, effects)
        self.assertIn("Type: Leader", str(leader_skill))

        # Test with explicit target type
        leader_skill_custom_target = LeaderSkill(name="Self Buff Leader",
                                   description="Boosts self.",
                                   target_type=SkillTargetType.SELF,
                                   effects=effects)
        self.assertEqual(leader_skill_custom_target.target_type, SkillTargetType.SELF)


if __name__ == '__main__':
    unittest.main()
