#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script for the Dungeon Adventurers game.
Currently used for testing and simulation purposes.
"""

from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element
from dungeon_adventurers.game_data.hero_templates import HERO_TEMPLATES, HERO_TEMPLATES_BY_ID
from dungeon_adventurers.entities.hero import Hero
from dungeon_adventurers.systems.gacha_system import GachaBanner
# We might need Item and Equipment for other tests later, but not for this gacha sim.
# from dungeon_adventurers.entities.item import Item
# from dungeon_adventurers.entities.equipment import Equipment, EquipmentSlot, ItemQuality
# from dungeon_adventurers.entities.skills import ActiveSkill, PassiveSkill, LeaderSkill, SkillTargetType


def run_gacha_simulation():
    """
    Sets up a sample GachaBanner and simulates some pulls.
    """
    print("Starting Gacha Simulation...")

    # 1. Define the hero pool for the banner based on available templates
    # We'll categorize them by rarity from HERO_TEMPLATES
    hero_pool_by_rarity_sim = {
        Rarity.R: [],
        Rarity.SR: [],
        Rarity.SSR: []
    }
    for template_id, template in HERO_TEMPLATES_BY_ID.items():
        if template["base_rarity"] in hero_pool_by_rarity_sim:
            hero_pool_by_rarity_sim[template["base_rarity"]].append(template_id)
        # else: # Handle N or UR if we add them to the pool dict
            # print(f"Warning: Template {template_id} has rarity {template['base_rarity']} not in banner pool dict.")

    # Ensure all rarities in the pool have at least one hero if they are to be pulled.
    # The GachaBanner __init__ checks for empty lists for rarities in hero_pool_by_rarity.
    # For this simulation, ensure that rarities in rate_table also have entries in hero_pool_by_rarity_sim.

    # If a Rarity might have 0% chance but is in hero_pool_by_rarity, it's fine.
    # If a Rarity has >0% chance in rate_table, it MUST have heroes in hero_pool_by_rarity_sim.

    # Filter out rarities from hero_pool_by_rarity_sim if they ended up empty
    # (e.g. if we had no SSR templates defined but SSR was in the dict)
    hero_pool_by_rarity_sim_filtered = {
        r: ids for r, ids in hero_pool_by_rarity_sim.items() if ids
    }
    if not hero_pool_by_rarity_sim_filtered.get(Rarity.SSR): # Example: if no SSR templates were added
        print("Warning: No SSR heroes in the pool for this simulation banner based on current templates.")


    # 2. Define the rate table for rarities
    # Make sure these rarities have heroes in hero_pool_by_rarity_sim_filtered
    # For example, if no SSR heroes, SSR rate must be 0.
    rate_table_sim = {
        Rarity.R: 0.79,   # 79%
        Rarity.SR: 0.20,  # 20%
        # Ensure there are SSR heroes in the pool before setting a non-zero rate
        Rarity.SSR: 0.01 if hero_pool_by_rarity_sim_filtered.get(Rarity.SSR) else 0.0
    }
    # Adjust R rate if SSR rate became 0 to ensure sum is 1.0
    if rate_table_sim[Rarity.SSR] == 0.0 and hero_pool_by_rarity_sim_filtered.get(Rarity.SSR) is None:
        print("Adjusting R rate as SSR pool is empty and SSR rate set to 0.")
        rate_table_sim[Rarity.R] += 0.01 # Add the SSR probability to R

    # Ensure sum is 1.0
    current_sum = sum(rate_table_sim.values())
    if abs(current_sum - 1.0) > 1e-9:
        print(f"Warning: Rate table sum is {current_sum}, adjusting R rate.")
        # Simple adjustment to R, assumes R is the largest probability
        diff = 1.0 - current_sum
        rate_table_sim[Rarity.R] += diff
        print(f"Adjusted R rate to {rate_table_sim[Rarity.R]:.2f}. New sum: {sum(rate_table_sim.values())}")


    # 3. Create the GachaBanner instance
    # Ensure hero_pool_by_rarity_sim_filtered only contains rarities present in rate_table_sim with >0 probability
    banner_hero_pool = {r: hero_pool_by_rarity_sim_filtered[r]
                        for r in rate_table_sim if r in hero_pool_by_rarity_sim_filtered and rate_table_sim[r] > 0}

    # If after filtering, a rarity in rate_table > 0 has no pool, GachaBanner init will fail.
    # This setup is a bit complex for a simple main.py, but good for robustness.

    try:
        standard_banner = GachaBanner(
            name="Standard Hero Recruitment",
            cost_per_pull=100,
            rate_table=rate_table_sim,
            hero_pool_by_rarity=banner_hero_pool, # Use the filtered pool
            pull_count_for_pity=200, # Example pity
            guaranteed_rarity_at_pity=Rarity.SSR
        )
    except ValueError as e:
        print(f"Error creating GachaBanner: {e}")
        print("Please check hero_templates.py to ensure SSR heroes exist if SSR rate > 0.")
        print("Current rate table for sim:", rate_table_sim)
        print("Current hero pool for sim:", banner_hero_pool)
        return # Exit if banner creation fails

    print(f"\nCreated Banner: {standard_banner}")
    print(f"Rate Table: { {r.name: p for r, p in standard_banner.rate_table.items()} }")
    print(f"Pity Counter: {standard_banner.pity_counter}/{standard_banner.pull_count_for_pity} for {standard_banner.guaranteed_rarity_at_pity.name}")

    # 4. Simulate a single pull
    print("\n--- Simulating a Single Pull ---")
    try:
        pulled_hero_single = standard_banner.perform_pull()
        print(f"Pulled: {pulled_hero_single.name} (Rarity: {pulled_hero_single.rarity.name}, Profession: {pulled_hero_single.profession.name})")
        print(f"  Base Stats: {pulled_hero_single.base_stats}")
        # print(f"  Template Skill IDs: {getattr(pulled_hero_single, 'template_skill_ids', 'Not set')}") # If we added this attr
        print(f"Pity Counter after pull: {standard_banner.pity_counter}/{standard_banner.pull_count_for_pity}")
    except Exception as e:
        print(f"Error during single pull: {e}")


    # 5. Simulate a multi-pull (e.g., 10 pulls)
    num_multi_pulls = 10
    print(f"\n--- Simulating a Multi-Pull ({num_multi_pulls} pulls) ---")
    try:
        pulled_heroes_multi = standard_banner.perform_multi_pull(num_multi_pulls)
        print(f"Results of {num_multi_pulls} pulls:")
        for i, hero in enumerate(pulled_heroes_multi):
            print(f"  {i+1}. {hero.name} (Rarity: {hero.rarity.name})")
        print(f"Pity Counter after multi-pull: {standard_banner.pity_counter}/{standard_banner.pull_count_for_pity}")
    except Exception as e:
        print(f"Error during multi-pull: {e}")

    print("\nGacha Simulation Finished.\n")


if __name__ == "__main__":
    # This structure allows main.py to be run as a script:
    # - From the project root: python -m dungeon_adventurers.main
    # - Or potentially directly: python dungeon_adventurers/main.py (if PYTHONPATH is set up)

    # The user reported ModuleNotFoundError when running `python main.py` from within `dungeon_adventurers`
    # The `python -m dungeon_adventurers.main` from root is the robust way.

    print("Executing main.py...")
    run_gacha_simulation()
