from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
# from kivy.lang import Builder # Not strictly needed if convention is followed or App loads kv directory

# Builder.load_file('dungeon_adventurers/ui/kv/loading_screen.kv') # Path from where Python is run

class LoadingScreen(Screen):
    """
    Initial loading screen for the game.
    Displays a loading message and transitions to the main menu.
    Kivy will look for 'loadingscreen.kv' or 'loading_screen.kv' based on class name.
    If App specifies kv_directory, then 'loading_screen.kv' should be found.
    """
    def on_enter(self, *args):
        """
        Called when the screen is entered.
        Schedule a transition to the main menu.
        """
        print("LoadingScreen: Entered. Scheduling transition to main_menu.")
        Clock.schedule_once(self.go_to_main_menu, 3) # Simulate 3 seconds of loading

    def go_to_main_menu(self, dt):
        """
        Transitions to the main menu screen.
        Assumes the ScreenManager is available via self.manager.
        """
        if self.manager:
            print("LoadingScreen: Transitioning to 'main_menu_screen'.")
            self.manager.current = 'main_menu_screen'
        else:
            print("LoadingScreen: ScreenManager not found. Cannot transition.")
