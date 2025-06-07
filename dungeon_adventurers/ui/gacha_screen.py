from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label # For adding to GridLayout
# from kivy.properties import ObjectProperty # Not using for now, self.ids is fine

# Import Gacha System components
from dungeon_adventurers.systems.gacha_system import GachaBanner
from dungeon_adventurers.game_data.hero_templates import HERO_TEMPLATES_BY_ID
from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element # Added Profession, Element for dummy hero
from dungeon_adventurers.entities.hero import Hero


class GachaScreen(Screen):
    """
    Screen for handling Gacha pulls and displaying results.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.banner = None # Will be initialized in on_enter
        self.player_currency = 10000 # Placeholder currency

    def on_enter(self):
        """
        Called when the screen is entered. Initialize banner and update labels.
        """
        print("GachaScreen: Entered.")
        if not self.banner: # Initialize banner only once or if it needs refreshing
            self.setup_banner()
        
        self.update_status_labels()
        self.clear_pull_results() # Clear previous results when screen is entered

    def setup_banner(self):
        """
        Sets up a default GachaBanner instance for this screen.
        This logic is similar to what was in main.py for simulation.
        """
        hero_pool_by_rarity_sim = {r: [] for r in Rarity} 
        for template_id, template in HERO_TEMPLATES_BY_ID.items():
            if template["base_rarity"] in hero_pool_by_rarity_sim:
                 hero_pool_by_rarity_sim[template["base_rarity"]].append(template_id)
        
        hero_pool_by_rarity_filtered = {
            r: ids for r, ids in hero_pool_by_rarity_sim.items() if ids
        }

        rate_table_sim = {
            Rarity.R: 0.79,
            Rarity.SR: 0.20,
            Rarity.SSR: 0.01 
        }

        final_hero_pool = {}
        final_rate_table = {}
        current_total_prob = 0.0

        for r_enum in [Rarity.SSR, Rarity.SR, Rarity.R]: 
            if r_enum in hero_pool_by_rarity_filtered and hero_pool_by_rarity_filtered[r_enum]:
                final_hero_pool[r_enum] = hero_pool_by_rarity_filtered[r_enum]
                final_rate_table[r_enum] = rate_table_sim.get(r_enum, 0.0)
                current_total_prob += final_rate_table[r_enum]
            else:
                if r_enum in rate_table_sim and rate_table_sim[r_enum] > 0.0: # Only warn if it had a rate
                    print(f"GachaScreen: Warning - Rarity {r_enum.name} has no heroes in hero_templates. Removing from banner rates.")
        
        if abs(current_total_prob - 1.0) > 1e-9 and current_total_prob > 0:
            if Rarity.R in final_rate_table and final_rate_table[Rarity.R] > 0 : # Check R is positive before adding diff
                diff = 1.0 - current_total_prob
                final_rate_table[Rarity.R] += diff
                print(f"GachaScreen: Adjusted Rarity.R probability by {diff:.4f} to make sum 1.0. New R rate: {final_rate_table[Rarity.R]:.4f}")
            else: # Fallback: simple normalization if R isn't there or was 0
                print(f"GachaScreen: Normalizing probabilities. Original sum: {current_total_prob:.4f}")
                for r_key in final_rate_table:
                    final_rate_table[r_key] /= current_total_prob
        
        if not final_hero_pool or not final_rate_table :
            print("GachaScreen: ERROR - Cannot create banner, no valid hero pool or rates after filtering.")
            self.banner = None
            return

        try:
            self.banner = GachaBanner(
                name="Standard Gacha",
                cost_per_pull=100, 
                rate_table=final_rate_table,
                hero_pool_by_rarity=final_hero_pool,
                pull_count_for_pity=100, 
                guaranteed_rarity_at_pity=Rarity.SSR
            )
            print("GachaScreen: Banner setup complete.")
        except ValueError as e:
            print(f"GachaScreen: Error creating GachaBanner: {e}")
            self.banner = None

    def update_status_labels(self):
        """Updates currency and pity labels on the screen."""
        if hasattr(self, 'ids') and self.ids: # Check if ids dictionary exists and is populated
            if 'currency_label' in self.ids:
                 self.ids.currency_label.text = f"Currency: {self.player_currency}"
            if 'pity_label' in self.ids:
                if self.banner:
                    self.ids.pity_label.text = f"Pity: {self.banner.pity_counter}/{self.banner.pull_count_for_pity} ({self.banner.guaranteed_rarity_at_pity.name})"
                else:
                    self.ids.pity_label.text = "Pity: Banner N/A"
        else:
            print("GachaScreen: self.ids not populated yet for status labels (update_status_labels).")


    def update_pull_results_display(self, pulled_heroes: list[Hero]):
        """Clears and updates the GridLayout with new hero pull results."""
        if not hasattr(self, 'ids') or not self.ids or 'pull_results_grid' not in self.ids:
            print("GachaScreen: pull_results_grid not found in self.ids (update_pull_results_display).")
            return
            
        grid = self.ids.pull_results_grid
        grid.clear_widgets()
        if not pulled_heroes:
            grid.add_widget(Label(text="No results to display.", size_hint_y=None, height='30dp'))
            return

        for hero in pulled_heroes:
            result_text = f"{hero.name} (Rarity: {hero.rarity.name}, Prof: {hero.profession.name})"
            label = Label(text=result_text, size_hint_y=None, height='30dp', color=(0.8,0.8,0.8,1)) # Light text for dark bg
            grid.add_widget(label)

    def clear_pull_results(self):
        if hasattr(self, 'ids') and self.ids and 'pull_results_grid' in self.ids:
            self.ids.pull_results_grid.clear_widgets()
            self.ids.pull_results_grid.add_widget(Label(text="Make a pull!", size_hint_y=None, height='30dp', color=(0.8,0.8,0.8,1)))
        else:
            print("GachaScreen: pull_results_grid not found in self.ids (clear_pull_results).")


    def pull_one_pressed(self):
        print("GachaScreen: 'Pull 1' pressed.")
        if not self.banner:
            print("GachaScreen: Banner not available for pull.")
            # Use dummy Hero for display if banner fails
            error_hero = Hero(name="Error: Banner Not Ready", rarity=Rarity.N, profession=Profession.WARRIOR, element=Element.FIRE)
            self.update_pull_results_display([error_hero])
            return

        cost = self.banner.cost_per_pull
        if self.player_currency >= cost:
            self.player_currency -= cost
            pulled_hero = self.banner.perform_pull()
            self.update_pull_results_display([pulled_hero])
            self.update_status_labels()
            print(f"GachaScreen: Pulled {pulled_hero.name}")
        else:
            print("GachaScreen: Not enough currency for Pull 1.")
            error_hero = Hero(name="Error: Not Enough Currency", rarity=Rarity.N, profession=Profession.WARRIOR, element=Element.FIRE)
            self.update_pull_results_display([error_hero])


    def pull_ten_pressed(self):
        print("GachaScreen: 'Pull 10' pressed.")
        if not self.banner:
            print("GachaScreen: Banner not available for multi-pull.")
            error_hero = Hero(name="Error: Banner Not Ready", rarity=Rarity.N, profession=Profession.WARRIOR, element=Element.FIRE)
            self.update_pull_results_display([error_hero] * 10) # Show 10 error messages
            return
            
        num_pulls = 10
        cost = self.banner.cost_per_pull * num_pulls 
        
        if self.player_currency >= cost:
            self.player_currency -= cost
            pulled_heroes = self.banner.perform_multi_pull(num_pulls)
            self.update_pull_results_display(pulled_heroes)
            self.update_status_labels()
            print(f"GachaScreen: Performed {num_pulls} pulls.")
        else:
            print("GachaScreen: Not enough currency for Pull 10.")
            error_hero = Hero(name="Error: Not Enough Currency", rarity=Rarity.N, profession=Profession.WARRIOR, element=Element.FIRE)
            self.update_pull_results_display([error_hero]) # Show one error message for this case

    def back_to_menu_pressed(self):
        print("GachaScreen: 'Back to Menu' pressed.")
        if self.manager:
            self.manager.current = 'main_menu_screen'
        else:
            print("GachaScreen: ScreenManager not found.")
