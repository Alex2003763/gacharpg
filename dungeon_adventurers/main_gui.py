#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Kivy application entry point for Dungeon Adventurers.
Manages screens and the overall GUI lifecycle.
"""

import kivy
kivy.require('1.11.1') # Specify Kivy version compatibility

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder
import os

# Import our custom screens
from dungeon_adventurers.ui.loading_screen import LoadingScreen
from dungeon_adventurers.ui.main_menu_screen import MainMenuScreen

KV_DIR = os.path.join(os.path.dirname(__file__), 'ui', 'kv')

class DungeonAdventurersApp(App):
    """
    Main application class for Dungeon Adventurers.
    """

    def build(self):
        """
        Builds the application's widget tree.
        """
        # Load the .kv files for our screens explicitly.
        # This ensures Kivy finds them, especially when they are in a subdirectory.
        Builder.load_file(os.path.join(KV_DIR, 'loading_screen.kv'))
        Builder.load_file(os.path.join(KV_DIR, 'main_menu_screen.kv'))

        # Create the screen manager
        sm = ScreenManager()
        # sm.transition = FadeTransition() # Optional: set a default transition

        # Add screens to the manager. The name given is used for switching.
        sm.add_widget(LoadingScreen(name='loading_screen'))
        sm.add_widget(MainMenuScreen(name='main_menu_screen'))

        # Set the initial screen
        sm.current = 'loading_screen'

        return sm

if __name__ == '__main__':
    print("Starting Dungeon Adventurers Kivy App...")
    DungeonAdventurersApp().run()
    print("Dungeon Adventurers Kivy App finished.")
