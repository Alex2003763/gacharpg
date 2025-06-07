#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the Gacha (summoning/pulling) system.
"""

# Imports will be added as classes are defined
from dungeon_adventurers.game_data.game_enums import Rarity # Example, likely needed
from dungeon_adventurers.game_data.hero_templates import HERO_TEMPLATES_BY_ID # Likely needed
from dungeon_adventurers.entities.hero import Hero # To instantiate heroes
import random

class GachaBanner:
    """
    Represents a specific gacha banner with its own pool of heroes and rates.
    """
    def __init__(self,
                 name: str,
                 cost_per_pull: int,
                 rate_table: dict[Rarity, float],
                 hero_pool_by_rarity: dict[Rarity, list[str]], # list of template_ids
                 pull_count_for_pity: int = 100, # e.g., 100 pulls for a guaranteed SSR
                 guaranteed_rarity_at_pity: Rarity = Rarity.SSR): # Rarity guaranteed at pity
        """
        Initializes a GachaBanner.

        Args:
            name (str): Name of the banner.
            cost_per_pull (int): Cost for a single pull.
            rate_table (dict[Rarity, float]): Probabilities for each rarity.
                                              Sum of probabilities should be 1.0.
            hero_pool_by_rarity (dict[Rarity, list[str]]):
                Maps rarity to a list of hero template_ids available at that rarity.
            pull_count_for_pity (int): Number of pulls to trigger pity.
            guaranteed_rarity_at_pity (Rarity): The rarity guaranteed when pity is hit.
        """
        if not name:
            raise ValueError("Banner name cannot be empty.")
        if cost_per_pull < 0:
            raise ValueError("Cost per pull cannot be negative.")
        if not rate_table or not all(isinstance(r, Rarity) for r in rate_table.keys()):
            raise ValueError("rate_table must be a non-empty dict with Rarity keys.")
        if not hero_pool_by_rarity or not all(isinstance(r, Rarity) for r in hero_pool_by_rarity.keys()):
            raise ValueError("hero_pool_by_rarity must be a non-empty dict with Rarity keys.")
        if pull_count_for_pity <= 0:
            raise ValueError("Pull count for pity must be positive.")

        # Validate that sum of probabilities in rate_table is close to 1.0
        if abs(sum(rate_table.values()) - 1.0) > 1e-9: # Using tolerance for float comparison
            raise ValueError(f"Sum of probabilities in rate_table must be 1.0. Got: {sum(rate_table.values())}")

        # Validate that all template_ids in hero_pool_by_rarity exist in HERO_TEMPLATES_BY_ID
        for rarity_key, template_ids in hero_pool_by_rarity.items():
            if not template_ids: # Ensure non-empty list of heroes for a rarity if defined
                 raise ValueError(f"Hero pool for rarity {rarity_key.name} cannot be empty if the rarity is in the pool.")
            for template_id in template_ids:
                if template_id not in HERO_TEMPLATES_BY_ID:
                    raise ValueError(f"Hero template_id '{template_id}' not found in HERO_TEMPLATES_BY_ID.")
                # Optional: Check if the template's base_rarity matches the pool's rarity_key
                # This adds complexity if a hero can appear in multiple rarity pools (e.g. rate-up)
                # For now, let's assume the pool is curated correctly.

        self.name = name
        self.cost_per_pull = cost_per_pull
        self.rate_table = rate_table
        self.hero_pool_by_rarity = hero_pool_by_rarity
        self.pull_count_for_pity = pull_count_for_pity
        self.guaranteed_rarity_at_pity = guaranteed_rarity_at_pity
        self.pity_counter = 0 # Increments with each pull

    def __str__(self) -> str:
        return f"GachaBanner: {self.name} (Cost: {self.cost_per_pull})"

    def perform_pull(self) -> Hero:
        """
        Performs a single pull from the banner.

        Returns:
            Hero: An instantiated Hero object based on the pull result.
        """
        self.pity_counter += 1

        # Determine pulled rarity
        # random.choices returns a list, so we take the first element.
        # It expects lists for population and weights.
        rarities = list(self.rate_table.keys())
        probabilities = list(self.rate_table.values())

        # Pity mechanism (simplified version for now: check if pity is hit)
        # A full pity system might guarantee a specific rarity if pity_counter hits pull_count_for_pity
        # and then reset the counter. For now, we just select based on rates.
        # A more complex pity would override pulled_rarity here.
        # For example:
        # if self.pity_counter >= self.pull_count_for_pity:
        #     pulled_rarity = self.guaranteed_rarity_at_pity
        #     self.pity_counter = 0 # Reset pity
        # else:
        #     pulled_rarity = random.choices(rarities, weights=probabilities, k=1)[0]
        #
        # For this step, let's keep it simpler and not implement the pity pull override yet,
        # just the counter increment. The actual pity logic can be a refinement.

        pulled_rarity = random.choices(rarities, weights=probabilities, k=1)[0]

        # Select a hero template from the chosen rarity
        available_template_ids = self.hero_pool_by_rarity.get(pulled_rarity)
        if not available_template_ids:
            # This should ideally not happen if validation in __init__ is correct
            # and all rarities in rate_table have corresponding entries in hero_pool_by_rarity
            # Fallback or raise error
            # For robustness, could try to pick from a default pool or next best rarity
            # Or, if this indicates a setup error, an exception is appropriate.
            # Let's assume __init__ validation ensures this won't be an issue for rarities with >0 probability.
             raise Exception(f"No hero templates defined for rarity {pulled_rarity.name} in banner '{self.name}', despite it being pullable.")

        selected_template_id = random.choice(available_template_ids)
        hero_template = HERO_TEMPLATES_BY_ID[selected_template_id]

        # Instantiate the Hero object from the template
        # Note: Hero __init__ takes name, rarity, profession, element, level
        # The template's base_rarity should match pulled_rarity, or be handled if they can differ (e.g. rate-ups)
        # For now, we assume template's base_rarity is the one we pulled.

        new_hero = Hero(name=hero_template["name"],
                        rarity=hero_template["base_rarity"], # This should ideally be pulled_rarity
                                                             # or we need to ensure template's base_rarity matches the pool its in.
                                                             # Let's use hero_template["base_rarity"] as source of truth for THIS hero.
                        profession=hero_template["profession"],
                        element=hero_template["element"]
                        # Level defaults to 1 in Hero constructor
                       )

        # Copy stats from template
        new_hero.base_stats = hero_template["base_stats_template"].copy()
        new_hero.advanced_stats = hero_template["advanced_stats_template"].copy()

        # Store skill IDs from template on the hero for later processing (optional)
        # The Hero class doesn't have a dedicated attribute for this yet.
        # We could add one, e.g., new_hero.template_skill_ids = hero_template["skill_ids"]
        # For now, actual Skill object assignment is deferred.
        # setattr(new_hero, 'template_skill_ids', hero_template.get("skill_ids", []))


        # If pity was hit and resulted in a specific rarity, reset counter
        # This logic would be more complex if pity guarantees a specific item vs just rarity.
        if self.pity_counter >= self.pull_count_for_pity and pulled_rarity == self.guaranteed_rarity_at_pity:
             # A simple interpretation: if you hit the pity count AND got the pity rarity (or better), reset.
             # More common: if you hit pity count, you GET pity_rarity, then reset.
             # Let's refine this: if pity_counter hits threshold, force guaranteed_rarity.
             pass # Full pity logic will be in a later refinement or next step if complex.

        return new_hero

    def perform_multi_pull(self, num_pulls: int) -> list[Hero]:
        """
        Performs a specified number of single pulls.

        Args:
            num_pulls (int): The number of pulls to perform.

        Returns:
            list[Hero]: A list of instantiated Hero objects from the pulls.
        """
        if not isinstance(num_pulls, int) or num_pulls <= 0:
            raise ValueError("Number of pulls must be a positive integer.")

        results = []
        for _ in range(num_pulls):
            results.append(self.perform_pull())
        return results

    # perform_pull() and perform_multi_pull() will be added in the next steps.
