# Dungeon Adventurers - Gacha RPG

This project is a modern-style gacha RPG, "Dungeon Adventurers," currently under development.

## Current Features

*   **Hero System:** Defines hero characters with attributes like rarity, profession, element, base stats, advanced stats, equipment slots, and skill slots.
*   **Item & Equipment System:** Defines items and equippable gear with stats and slots. Heroes can equip and unequip items.
*   **Skills System (Foundational):** Defines structures for active, passive, and leader skills with names, descriptions, types, targets, and effects. Heroes can have skills assigned.
*   **Gacha System (Basic):** Allows creation of gacha banners with configurable hero pools and rarity rates. Heroes can be "pulled" from these banners. Hero stats are based on predefined templates.

## Running the Simulation

The primary way to see the current systems in action is by running the main simulation script. This script currently demonstrates the Gacha system by creating a sample banner and performing simulated hero pulls.

**Prerequisites:**
*   Python 3.10 or higher (or the Python version supported by your current development environment).

**Steps to Run:**

1.  **Clone the Repository:**
    ```bash
    # Replace <repository_url> with the actual URL from your Git provider
    # git clone <repository_url>
    # cd <repository_directory_name>
    ```
    (Assuming you have already cloned or have access to the project files.)

2.  **Navigate to the Project Root:**
    Ensure you are in the main project directory. This is the directory that *contains* the `dungeon_adventurers` package directory (e.g., if your project path is `C:\Users\YourUser\Desktop\gacharpg`, you should be in `gacharpg`).

3.  **Run `main.py` as a Module:**
    Execute the following command from the project root directory:
    ```bash
    python -m dungeon_adventurers.main
    ```
    This will run the gacha simulation defined in `dungeon_adventurers/main.py` and print the output to your console.

## Development & Testing

*   **Unit Tests:** The project includes unit tests for various components. You can run all tests using Python's built-in `unittest` module's discovery feature from the project root:
    ```bash
    python -m unittest discover tests
    ```
    Alternatively, you can run specific test files:
    ```bash
    python -m unittest tests.test_hero # Example for hero tests
    python -m unittest tests.test_gacha_system # Example for gacha system tests
    ```

## Next Steps (Planned Features from GDD)

*   Full Pity System for Gacha.
*   Hero Leveling and Stat Progression.
*   Skill effect implementation.
*   Basic Combat System.
*   Dungeon Exploration.
*   User Interface (GUI).
*   And much more from the original Game Design Document!


## Running the GUI Application (Kivy)

**Prerequisites:**
*   Python 3.10 or higher.
*   Kivy: Install using `python -m pip install "kivy[base]" kivy_examples` or `python -m pip install -r requirements.txt`.

**To Run the GUI:**
1.  Navigate to the project root directory.
2.  Execute: `python -m dungeon_adventurers.main_gui`

*Note: The original `python -m dungeon_adventurers.main` command still runs the console-based Gacha simulation.*
