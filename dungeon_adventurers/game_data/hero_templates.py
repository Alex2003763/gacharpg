from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element

# Hero templates define the blueprint for heroes that can be summoned.
# When a hero is summoned, a Hero instance is created based on one of these templates.

# For now, skills are represented by placeholder IDs.
# In a fuller implementation, these IDs would map to actual Skill objects/templates.

HERO_TEMPLATES = [
    {
        "template_id": "HT001",
        "name": "Valiant Knight",
        "base_rarity": Rarity.R,
        "profession": Profession.WARRIOR,
        "element": Element.LIGHT,
        "base_stats_template": {"HP": 120, "Attack": 12, "Defense": 10, "Speed": 8},
        "advanced_stats_template": {"CritRate": 0.05, "CritDamage": 1.5, "HitChance": 1.0, "Evasion": 0.05, "EffectResistance": 0.0},
        "skill_ids": ["skill_slash", "skill_warrior_passive_hp_up"] # Placeholder skill IDs
    },
    {
        "template_id": "HT002",
        "name": "Mystic Mage",
        "base_rarity": Rarity.R,
        "profession": Profession.MAGE,
        "element": Element.DARK,
        "base_stats_template": {"HP": 90, "Attack": 15, "Defense": 6, "Speed": 10},
        "advanced_stats_template": {"CritRate": 0.05, "CritDamage": 1.6, "HitChance": 1.0, "Evasion": 0.05, "EffectResistance": 0.0},
        "skill_ids": ["skill_dark_bolt", "skill_mage_passive_mana_regen"]
    },
    {
        "template_id": "HT003",
        "name": "Shadow Assassin",
        "base_rarity": Rarity.SR,
        "profession": Profession.ASSASSIN,
        "element": Element.DARK,
        "base_stats_template": {"HP": 100, "Attack": 18, "Defense": 7, "Speed": 15},
        "advanced_stats_template": {"CritRate": 0.10, "CritDamage": 1.75, "HitChance": 1.0, "Evasion": 0.1, "EffectResistance": 0.0},
        "skill_ids": ["skill_shadow_strike", "skill_assassin_passive_crit_up", "skill_leader_crit_chance"]
    },
    {
        "template_id": "HT004",
        "name": "Guardian Defender",
        "base_rarity": Rarity.SR,
        "profession": Profession.TANK,
        "element": Element.GRASS,
        "base_stats_template": {"HP": 200, "Attack": 8, "Defense": 15, "Speed": 5},
        "advanced_stats_template": {"CritRate": 0.03, "CritDamage": 1.5, "HitChance": 1.0, "Evasion": 0.03, "EffectResistance": 0.1},
        "skill_ids": ["skill_taunt", "skill_tank_passive_def_up"]
    },
    {
        "template_id": "HT005",
        "name": "Celestial Healer",
        "base_rarity": Rarity.SSR,
        "profession": Profession.SUPPORT,
        "element": Element.LIGHT,
        "base_stats_template": {"HP": 150, "Attack": 10, "Defense": 8, "Speed": 12},
        "advanced_stats_template": {"CritRate": 0.05, "CritDamage": 1.5, "HitChance": 1.0, "Evasion": 0.05, "EffectResistance": 0.15},
        "skill_ids": ["skill_group_heal", "skill_support_passive_resist_up", "skill_leader_team_heal_potency"]
    }
]

# A dictionary for quick lookup by template_id might be useful too
HERO_TEMPLATES_BY_ID = {tpl["template_id"]: tpl for tpl in HERO_TEMPLATES}

# Example of how skill details might be stored (outside the scope of this specific step, but for context)
# SKILL_DEFINITIONS = {
#     "skill_slash": {"name": "Slash", "description": "...", type: ActiveSkill, ...},
#     ...
# }

if __name__ == '__main__':
    # Quick check to see if templates are accessible
    for template in HERO_TEMPLATES:
        print(f"Loaded Hero Template: {template['name']} ({template['base_rarity'].name})")

    if "HT001" in HERO_TEMPLATES_BY_ID:
        print(f"Lookup successful for HT001: {HERO_TEMPLATES_BY_ID['HT001']['name']}")
