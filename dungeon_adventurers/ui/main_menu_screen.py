from kivy.uix.screenmanager import Screen
from kivy.app import App # To quit the app
# from kivy.lang import Builder

# Builder.load_file('dungeon_adventurers/ui/kv/main_menu_screen.kv') # If needed

class MainMenuScreen(Screen):
    """
    Main menu screen for the game.
    Provides options to start, view options (placeholder), or quit.
    """
    def on_start_sim_press(self):
        """
        Called when the 'Start Gacha Simulation' button is pressed.
        For now, just prints a message. Later, could transition to a simulation screen
        or trigger the gacha logic if UI is integrated with it.
        """
        print("MainMenuScreen: 'Start Gacha Simulation' button pressed!")
        # Placeholder: In a full GUI, you might switch to another screen:
        # if self.manager:
        #     self.manager.current = 'gacha_simulation_screen'

    def on_options_press(self):
        """
        Called when the 'Options' button is pressed.
        Currently non-functional.
        """
        print("MainMenuScreen: 'Options' button pressed! (Not implemented yet)")

    def on_quit_press(self):
        """
        Called when the 'Quit' button is pressed.
        Stops the Kivy application.
        """
        print("MainMenuScreen: 'Quit' button pressed! Exiting application.")
        App.get_running_app().stop()
