import unittest
from unittest.mock import patch, MagicMock
import random # Still needed for some direct random calls if not all are patched

from dungeon_adventurers.systems.gacha_system import GachaBanner
from dungeon_adventurers.game_data.game_enums import Rarity, Profession, Element
from dungeon_adventurers.game_data.hero_templates import HERO_TEMPLATES_BY_ID, HERO_TEMPLATES
from dungeon_adventurers.entities.hero import Hero

class TestGachaBanner(unittest.TestCase):

    def setUp(self):
        # Use a subset of actual templates for testing to keep it manageable
        self.test_hero_templates_by_id = {
            "HT001": {"template_id": "HT001", "name": "Valiant Knight", "base_rarity": Rarity.R,
                      "profession": Profession.WARRIOR, "element": Element.LIGHT,
                      "base_stats_template": {"HP": 100}, "advanced_stats_template": {"CritRate": 0.05}, "skill_ids": []},
            "HT002": {"template_id": "HT002", "name": "Mystic Mage", "base_rarity": Rarity.R,
                      "profession": Profession.MAGE, "element": Element.DARK,
                      "base_stats_template": {"HP": 90}, "advanced_stats_template": {"CritRate": 0.06}, "skill_ids": []},
            "HT003": {"template_id": "HT003", "name": "Shadow Assassin", "base_rarity": Rarity.SR,
                      "profession": Profession.ASSASSIN, "element": Element.DARK,
                      "base_stats_template": {"HP": 110}, "advanced_stats_template": {"CritRate": 0.1}, "skill_ids": []},
            "HT005": {"template_id": "HT005", "name": "Celestial Healer", "base_rarity": Rarity.SSR,
                      "profession": Profession.SUPPORT, "element": Element.LIGHT,
                      "base_stats_template": {"HP": 150}, "advanced_stats_template": {"CritRate": 0.03}, "skill_ids": []}
        }

        # Patch HERO_TEMPLATES_BY_ID for the duration of tests in this class
        # This way, GachaBanner uses our controlled subset.
        self.patcher = patch('dungeon_adventurers.systems.gacha_system.HERO_TEMPLATES_BY_ID', self.test_hero_templates_by_id)
        self.mock_hero_templates = self.patcher.start()

        self.rate_table = {
            Rarity.R: 0.70,
            Rarity.SR: 0.25,
            Rarity.SSR: 0.05
        }
        self.hero_pool = {
            Rarity.R: ["HT001", "HT002"],
            Rarity.SR: ["HT003"],
            Rarity.SSR: ["HT005"]
        }
        self.banner = GachaBanner(name="Test Banner",
                                  cost_per_pull=100,
                                  rate_table=self.rate_table,
                                  hero_pool_by_rarity=self.hero_pool,
                                  pull_count_for_pity=10,
                                  guaranteed_rarity_at_pity=Rarity.SSR)

    def tearDown(self):
        self.patcher.stop() # Important to stop the patch

    def test_gacha_banner_creation_valid(self):
        self.assertEqual(self.banner.name, "Test Banner")
        self.assertEqual(self.banner.cost_per_pull, 100)
        self.assertEqual(self.banner.rate_table, self.rate_table)
        self.assertEqual(self.banner.hero_pool_by_rarity, self.hero_pool)
        self.assertEqual(self.banner.pity_counter, 0)

    def test_gacha_banner_creation_invalid_rate_sum(self):
        invalid_rates = {Rarity.R: 0.5, Rarity.SR: 0.3} # Sum is 0.8
        with self.assertRaisesRegex(ValueError, "Sum of probabilities in rate_table must be 1.0"):
            GachaBanner("Bad Rates", 100, invalid_rates, self.hero_pool)

    def test_gacha_banner_creation_invalid_template_id(self):
        invalid_pool = {Rarity.R: ["HTUNKNOWN"], Rarity.SR: [], Rarity.SSR: []} # HTUNKNOWN doesn't exist
        rates = {Rarity.R: 1.0, Rarity.SR: 0.0, Rarity.SSR: 0.0}
        with self.assertRaisesRegex(ValueError, "Hero template_id 'HTUNKNOWN' not found"):
            GachaBanner("Bad Pool", 100, rates, invalid_pool)

    def test_gacha_banner_creation_empty_hero_list_for_rarity(self):
        pool_with_empty_r_list = {Rarity.R: [], Rarity.SR: ["HT003"], Rarity.SSR: ["HT005"]}
        rates = {Rarity.R: 0.5, Rarity.SR: 0.3, Rarity.SSR: 0.2} # R has a rate > 0
        with self.assertRaisesRegex(ValueError, "Hero pool for rarity R cannot be empty"):
            GachaBanner("Empty R List", 100, rates, pool_with_empty_r_list)


    @patch('random.choices') # Mocks random.choices used for rarity selection
    @patch('random.choice')  # Mocks random.choice used for hero selection within rarity
    def test_perform_pull_ssr_outcome(self, mock_choice, mock_choices):
        # Configure mocks:
        # 1. random.choices (for rarity) returns [Rarity.SSR]
        mock_choices.return_value = [Rarity.SSR]
        # 2. random.choice (for hero template ID from SSR pool) returns "HT005"
        mock_choice.return_value = "HT005"

        pulled_hero = self.banner.perform_pull()

        mock_choices.assert_called_once_with(list(self.rate_table.keys()), weights=list(self.rate_table.values()), k=1)
        mock_choice.assert_called_once_with(self.hero_pool[Rarity.SSR])

        self.assertIsInstance(pulled_hero, Hero)
        self.assertEqual(pulled_hero.name, "Celestial Healer") # From HT005
        self.assertEqual(pulled_hero.rarity, Rarity.SSR)
        self.assertEqual(pulled_hero.profession, Profession.SUPPORT)
        self.assertEqual(pulled_hero.base_stats, self.test_hero_templates_by_id["HT005"]["base_stats_template"])
        self.assertEqual(self.banner.pity_counter, 1)

    @patch('random.choices')
    @patch('random.choice')
    def test_perform_pull_r_outcome(self, mock_choice, mock_choices):
        mock_choices.return_value = [Rarity.R]
        mock_choice.return_value = "HT001" # Valiant Knight

        pulled_hero = self.banner.perform_pull()

        mock_choices.assert_called_once_with(list(self.rate_table.keys()), weights=list(self.rate_table.values()), k=1)
        mock_choice.assert_called_once_with(self.hero_pool[Rarity.R])

        self.assertIsInstance(pulled_hero, Hero)
        self.assertEqual(pulled_hero.name, "Valiant Knight")
        self.assertEqual(pulled_hero.rarity, Rarity.R)
        self.assertEqual(self.banner.pity_counter, 1)

    def test_perform_multi_pull_valid_number(self):
        num_pulls = 3
        # We don't need to mock random here if we're just testing the loop and return type/count
        # The individual pulls' randomness is tested in test_perform_pull_...
        # However, perform_pull itself uses random, so results will vary.
        # For consistency, or to test specific multi-pull scenarios, mocking perform_pull might be needed.
        # Here, we'll rely on perform_pull working as tested by other methods.

        # To make this test deterministic without mocking perform_pull itself,
        # we can mock the random functions it uses, repeatedly.

        # Let's simplify: just check count and type for multi_pull.
        # Assume perform_pull works and returns valid heroes.

        with patch.object(self.banner, 'perform_pull', autospec=True) as mock_perform_pull:
            # Configure perform_pull to return a dummy Hero-like object or a real one if needed
            # For this test, we only care it's called N times.
            # Let's make it return a simple mock Hero to avoid full Hero instantiation logic here.
            mock_hero_instance = MagicMock(spec=Hero)
            mock_hero_instance.name = "Mocked Hero"
            mock_perform_pull.return_value = mock_hero_instance

            results = self.banner.perform_multi_pull(num_pulls)

            self.assertEqual(mock_perform_pull.call_count, num_pulls)
            self.assertEqual(len(results), num_pulls)
            for hero in results:
                self.assertIsInstance(hero, MagicMock) # Because we mocked perform_pull's return

    def test_perform_multi_pull_invalid_number(self):
        with self.assertRaisesRegex(ValueError, "Number of pulls must be a positive integer."):
            self.banner.perform_multi_pull(0)
        with self.assertRaisesRegex(ValueError, "Number of pulls must be a positive integer."):
            self.banner.perform_multi_pull(-1)

    # Pity mechanism tests would go here once the pity logic in perform_pull is fully implemented.
    # For example:
    # @patch('random.choices')
    # @patch('random.choice')
    # def test_perform_pull_hits_pity(self, mock_choice, mock_choices):
    #     self.banner.pity_counter = self.banner.pull_count_for_pity - 1 # One pull away from pity
    #     # Mock choices to return a non-pity rarity initially
    #     mock_choices.return_value = [Rarity.R]
    #     mock_choice.return_value = "HT001" # R hero

    #     # If pity logic forces SSR at pity:
    #     # Expected: mock_choice for SSR pool ("HT005") should be called.
    #     # This needs perform_pull to have the pity override logic.

    #     # For now, this test would just show pity_counter incrementing.
    #     # When pity is implemented, this test would verify that HT005 (SSR) is returned.
    #     # pulled_hero = self.banner.perform_pull()
    #     # self.assertEqual(pulled_hero.rarity, Rarity.SSR) # Assuming pity guarantees SSR
    #     # self.assertEqual(self.banner.pity_counter, 0) # Pity resets


if __name__ == '__main__':
    unittest.main()
