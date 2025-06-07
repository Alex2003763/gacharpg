from enum import Enum # Required for type hinting if enums are used directly
from dungeon_adventurers.game_data.game_enums import SkillType, SkillTargetType, Element # Element for skill effects

class Skill:
    """
    Represents a base skill in the game.
    This class is intended to be inherited by more specific skill types (Active, Passive, Leader).
    """
    def __init__(self,
                 name: str,
                 description: str,
                 skill_type: SkillType,
                 target_type: SkillTargetType,
                 effects: list[dict]):
        """
        Initializes a new Skill.

        Args:
            name (str): The name of the skill.
            description (str): A description of what the skill does.
            skill_type (SkillType): The type of the skill (e.g., ACTIVE, PASSIVE).
            target_type (SkillTargetType): Who the skill targets.
            effects (list[dict]): A list of dictionaries defining the skill's effects.
                Example: [{"effect_type": "damage", "value": 100, "element": Element.FIRE},
                          {"effect_type": "heal", "percentage": 0.10, "target_stat": "HP"}]
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Skill name must be a non-empty string.")
        if not isinstance(description, str):
            raise ValueError("Skill description must be a string.")
        if not isinstance(skill_type, SkillType):
            raise ValueError("skill_type must be an instance of SkillType enum.")
        if not isinstance(target_type, SkillTargetType):
            raise ValueError("target_type must be an instance of SkillTargetType enum.")
        if not isinstance(effects, list) or not all(isinstance(e, dict) for e in effects):
            raise ValueError("effects must be a list of dictionaries.")

        self.name = name
        self.description = description
        self.skill_type = skill_type
        self.target_type = target_type
        self.effects = effects # Actual processing of these effects will be in the combat system

    def __str__(self) -> str:
        return (f"{self.skill_type.name} Skill: {self.name} ({self.target_type.name}) - {self.description}\n"
                f"  Effects: {self.effects}")

    def get_effects_description(self) -> str:
        """
        Provides a more human-readable description of the skill's effects.
        (This can be expanded later for more detailed descriptions).
        """
        if not self.effects:
            return "No specific effects defined."

        descriptions = []
        for effect in self.effects:
            etype = effect.get("effect_type", "Unknown effect")
            val = effect.get("value")
            percent = effect.get("percentage")
            element = effect.get("element")
            stat = effect.get("target_stat")

            desc_str = f"{etype.capitalize()}"
            if val is not None:
                desc_str += f" for {val}"
            if percent is not None:
                desc_str += f" for {percent*100:.0f}%"
            if stat is not None:
                desc_str += f" of {stat}"
            if element is not None:
                # Assuming element is an Enum member, get its name
                element_name = element.name if isinstance(element, Enum) else str(element)
                desc_str += f" ({element_name} element)"
            descriptions.append(desc_str)
        return "; ".join(descriptions)

class ActiveSkill(Skill):
    """
    Represents an active skill that a hero can use, typically with a cost or cooldown.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 target_type: SkillTargetType,
                 effects: list[dict],
                 cooldown: int = 0,
                 energy_cost: int = 0):
        super().__init__(name, description, SkillType.ACTIVE, target_type, effects)

        if not isinstance(cooldown, int) or cooldown < 0:
            raise ValueError("Cooldown must be a non-negative integer.")
        if not isinstance(energy_cost, int) or energy_cost < 0:
            raise ValueError("Energy cost must be a non-negative integer.")

        self.cooldown = cooldown
        self.current_cooldown = 0 # Runtime state, 0 means available
        self.energy_cost = energy_cost

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str}\n"
                f"  Type: Active | Cost: {self.energy_cost} Energy | Cooldown: {self.cooldown} turns")

    def put_on_cooldown(self):
        """Sets the skill on cooldown."""
        self.current_cooldown = self.cooldown

    def reduce_cooldown(self, turns: int = 1):
        """Reduces the current cooldown by a number of turns."""
        self.current_cooldown = max(0, self.current_cooldown - turns)

    def is_available(self) -> bool:
        """Checks if the skill is currently available (not on cooldown)."""
        return self.current_cooldown == 0


class PassiveSkill(Skill):
    """
    Represents a passive skill that provides constant benefits or triggers automatically.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 target_type: SkillTargetType, # Often SELF, but could be ALLY_TEAM for auras
                 effects: list[dict]):
        super().__init__(name, description, SkillType.PASSIVE, target_type, effects)

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str}\n"
                f"  Type: Passive")


class LeaderSkill(Skill):
    """
    Represents a leader skill that is active when the hero is in the leader position.
    """
    def __init__(self,
                 name: str,
                 description: str,
                  effects: list[dict],
                 # Leader skills often target ALLY_TEAM or specific types of allies
                  target_type: SkillTargetType = SkillTargetType.ALLY_TEAM):
        super().__init__(name, description, SkillType.LEADER, target_type, effects)

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str}\n"
                f"  Type: Leader")
