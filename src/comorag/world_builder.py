"""
WorldBuilder - Manages world-building elements
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Location:
    """Location in the story world"""
    name: str
    description: str = ""
    type: str = "generic"  # city, building, natural, etc.
    significance: str = ""
    appears_in_chapters: List[int] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'significance': self.significance,
            'appears_in_chapters': self.appears_in_chapters,
            'notes': self.notes
        }


@dataclass
class WorldRule:
    """Rule or law of the story world"""
    name: str
    description: str
    category: str = "general"  # magic, physics, social, political, etc.
    exceptions: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'exceptions': self.exceptions,
            'notes': self.notes
        }


class WorldBuilder:
    """
    Manages world-building elements.

    Features:
    - Location management
    - World rules and laws
    - Lore and history
    - Consistency tracking
    """

    def __init__(self, llm_model, config=None):
        """
        Initialize WorldBuilder

        Args:
            llm_model: LLM for generating world details
            config: Configuration object
        """
        self.llm_model = llm_model
        self.config = config

        # Storage
        self.locations: Dict[str, Location] = {}
        self.rules: Dict[str, WorldRule] = {}
        self.lore: List[Dict[str, Any]] = []
        self.history: List[Dict[str, Any]] = []

        logger.info("WorldBuilder initialized")

    def add_location(
        self,
        name: str,
        description: str = "",
        location_type: str = "generic",
        significance: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a location

        Args:
            name: Location name
            description: Detailed description
            location_type: Type of location
            significance: Story significance
            **kwargs: Additional attributes

        Returns:
            Location data dictionary
        """
        location = Location(
            name=name,
            description=description,
            type=location_type,
            significance=significance,
            notes=kwargs.get('notes', '')
        )

        self.locations[name] = location
        logger.info(f"Added location: {name}")

        return location.to_dict()

    def add_rule(
        self,
        name: str,
        description: str,
        category: str = "general",
        exceptions: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a world rule

        Args:
            name: Rule name
            description: Rule description
            category: Rule category
            exceptions: List of exceptions
            **kwargs: Additional attributes

        Returns:
            Rule data dictionary
        """
        rule = WorldRule(
            name=name,
            description=description,
            category=category,
            exceptions=exceptions or [],
            notes=kwargs.get('notes', '')
        )

        self.rules[name] = rule
        logger.info(f"Added world rule: {name}")

        return rule.to_dict()

    def add_lore(
        self,
        title: str,
        content: str,
        category: str = "general",
        **kwargs
    ):
        """
        Add lore/background information

        Args:
            title: Lore title
            content: Lore content
            category: Category (mythology, history, culture, etc.)
            **kwargs: Additional attributes
        """
        lore_item = {
            'title': title,
            'content': content,
            'category': category,
            'created_at': datetime.now().isoformat(),
            **kwargs
        }

        self.lore.append(lore_item)
        logger.info(f"Added lore: {title}")

    def get_location(self, name: str) -> Optional[Dict[str, Any]]:
        """Get location by name"""
        location = self.locations.get(name)
        return location.to_dict() if location else None

    def get_all_locations(self) -> List[Dict[str, Any]]:
        """Get all locations"""
        return [loc.to_dict() for loc in self.locations.values()]

    def get_rule(self, name: str) -> Optional[Dict[str, Any]]:
        """Get rule by name"""
        rule = self.rules.get(name)
        return rule.to_dict() if rule else None

    def get_all_rules(self) -> List[Dict[str, Any]]:
        """Get all world rules"""
        return [rule.to_dict() for rule in self.rules.values()]

    def get_lore_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get lore by category"""
        return [lore for lore in self.lore if lore['category'] == category]

    def generate_location_description(
        self,
        location_name: str,
        location_type: str = "generic",
        mood: str = "neutral",
        max_tokens: int = 500
    ) -> str:
        """
        Generate detailed location description using LLM

        Args:
            location_name: Name of location
            location_type: Type of location
            mood: Desired mood
            max_tokens: Maximum tokens

        Returns:
            Generated description
        """
        if not self.llm_model:
            return f"[{location_name}: No LLM available for generation]"

        prompt = f"""Describe the location: {location_name}

Type: {location_type}
Mood: {mood}

Write a vivid, detailed description that brings this location to life. Include:
- Visual details
- Atmosphere
- Sounds and smells
- Notable features

Write the description:
"""

        try:
            description = self.llm_model.generate(prompt, max_tokens=max_tokens)
            logger.info(f"Generated description for location: {location_name}")
            return description.strip()

        except Exception as e:
            logger.error(f"Failed to generate location description: {e}")
            return f"[{location_name}]"

    def get_summary(self) -> str:
        """Get world-building summary"""
        num_locations = len(self.locations)
        num_rules = len(self.rules)
        num_lore = len(self.lore)

        summary = f"""
World-Building Summary:
----------------------
Locations: {num_locations}
World Rules: {num_rules}
Lore Entries: {num_lore}
        """.strip()

        return summary
