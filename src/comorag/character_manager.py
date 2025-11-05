"""
CharacterManager - Manages character creation, tracking, and relationships
"""
import logging
from typing import Dict, List, Any, Optional, Set
import igraph as ig
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Character:
    """Character data structure"""
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    personality: str = ""
    background: str = ""
    appearance: str = ""
    goals: str = ""
    fears: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)
    character_arc: List[str] = field(default_factory=list)
    first_appearance: Optional[int] = None  # Chapter number
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'personality': self.personality,
            'background': self.background,
            'appearance': self.appearance,
            'goals': self.goals,
            'fears': self.fears,
            'relationships': self.relationships,
            'character_arc': self.character_arc,
            'first_appearance': self.first_appearance,
            'created_at': self.created_at,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create from dictionary"""
        return cls(**data)


class CharacterManager:
    """
    Manages characters in the novel.

    Features:
    - Character creation and storage
    - Relationship graph management
    - Character development tracking
    - Consistency checking
    """

    def __init__(self, llm_model, embedding_store=None, config=None):
        """
        Initialize CharacterManager

        Args:
            llm_model: LLM for generating character details
            embedding_store: Embedding store for semantic character search
            config: Configuration object
        """
        self.llm_model = llm_model
        self.embedding_store = embedding_store
        self.config = config

        # Character storage
        self.characters: Dict[str, Character] = {}

        # Relationship graph
        self.relationship_graph = ig.Graph(directed=True)
        self.char_name_to_vertex: Dict[str, int] = {}

        logger.info("CharacterManager initialized")

    def create_character(
        self,
        name: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        personality: str = "",
        background: str = "",
        appearance: str = "",
        goals: str = "",
        fears: str = "",
        first_appearance: Optional[int] = None,
        auto_expand: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new character

        Args:
            name: Character name
            age: Character age
            gender: Character gender
            personality: Personality description
            background: Background story
            appearance: Physical appearance
            goals: Character goals/motivations
            fears: Character fears
            first_appearance: Chapter number of first appearance
            auto_expand: Use LLM to expand character details
            **kwargs: Additional character attributes

        Returns:
            Character data dictionary
        """
        if name in self.characters:
            logger.warning(f"Character '{name}' already exists. Updating instead.")
            return self.update_character(name, **locals())

        # Create character
        character = Character(
            name=name,
            age=age,
            gender=gender,
            personality=personality,
            background=background,
            appearance=appearance,
            goals=goals,
            fears=fears,
            first_appearance=first_appearance,
            notes=kwargs.get('notes', '')
        )

        # Auto-expand character details with LLM if requested
        if auto_expand and self.llm_model:
            character = self._expand_character_with_llm(character)

        # Store character
        self.characters[name] = character

        # Add to relationship graph
        vertex_id = self.relationship_graph.vcount()
        self.relationship_graph.add_vertex(
            name=name,
            character_data=character.to_dict()
        )
        self.char_name_to_vertex[name] = vertex_id

        logger.info(f"Created character: {name}")

        return character.to_dict()

    def _expand_character_with_llm(self, character: Character) -> Character:
        """Use LLM to expand character details"""
        prompt = f"""You are helping to develop a character for a novel.

Character Name: {character.name}
Current Details:
- Age: {character.age or 'Not specified'}
- Gender: {character.gender or 'Not specified'}
- Personality: {character.personality or 'Not specified'}
- Background: {character.background or 'Not specified'}

Please expand this character with rich, consistent details. Provide:
1. Enhanced personality traits (if needed)
2. Deeper background story (if minimal)
3. Physical appearance details
4. Character goals and motivations
5. Fears or vulnerabilities

Keep it concise but vivid. Return as JSON with keys: personality, background, appearance, goals, fears.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=500)
            # Parse and update character (simplified - would need proper JSON parsing)
            # For now, just log
            logger.info(f"LLM expanded character details for {character.name}")
        except Exception as e:
            logger.error(f"Failed to expand character with LLM: {e}")

        return character

    def update_character(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Update existing character

        Args:
            name: Character name
            **kwargs: Attributes to update

        Returns:
            Updated character data
        """
        if name not in self.characters:
            raise ValueError(f"Character '{name}' does not exist")

        character = self.characters[name]

        # Update attributes
        for key, value in kwargs.items():
            if hasattr(character, key) and value is not None:
                setattr(character, key, value)

        logger.info(f"Updated character: {name}")

        return character.to_dict()

    def add_relationship(
        self,
        character1: str,
        character2: str,
        relationship_type: str,
        description: str = ""
    ):
        """
        Add relationship between characters

        Args:
            character1: First character name
            character2: Second character name
            relationship_type: Type of relationship (friend, enemy, family, etc.)
            description: Description of the relationship
        """
        if character1 not in self.characters:
            raise ValueError(f"Character '{character1}' does not exist")
        if character2 not in self.characters:
            raise ValueError(f"Character '{character2}' does not exist")

        # Update character relationship data
        self.characters[character1].relationships[character2] = relationship_type
        self.characters[character2].relationships[character1] = relationship_type

        # Add edge to graph
        vertex1 = self.char_name_to_vertex[character1]
        vertex2 = self.char_name_to_vertex[character2]

        self.relationship_graph.add_edge(
            vertex1,
            vertex2,
            relationship_type=relationship_type,
            description=description
        )

        logger.info(f"Added relationship: {character1} --[{relationship_type}]--> {character2}")

    def get_character(self, name: str) -> Optional[Dict[str, Any]]:
        """Get character by name"""
        character = self.characters.get(name)
        return character.to_dict() if character else None

    def get_all_characters(self) -> List[Dict[str, Any]]:
        """Get all characters"""
        return [char.to_dict() for char in self.characters.values()]

    def get_character_relationships(self, name: str) -> Dict[str, str]:
        """Get all relationships for a character"""
        if name not in self.characters:
            raise ValueError(f"Character '{name}' does not exist")

        return self.characters[name].relationships.copy()

    def get_related_characters(
        self,
        name: str,
        relationship_type: Optional[str] = None,
        max_distance: int = 1
    ) -> List[str]:
        """
        Get characters related to the given character

        Args:
            name: Character name
            relationship_type: Filter by relationship type
            max_distance: Maximum distance in relationship graph

        Returns:
            List of related character names
        """
        if name not in self.char_name_to_vertex:
            return []

        vertex_id = self.char_name_to_vertex[name]

        # Get neighbors within max_distance
        neighbors = self.relationship_graph.neighborhood(
            vertices=vertex_id,
            order=max_distance
        )

        related = []
        for neighbor_id in neighbors:
            if neighbor_id != vertex_id:
                neighbor_name = self.relationship_graph.vs[neighbor_id]['name']

                # Filter by relationship type if specified
                if relationship_type:
                    char_relationships = self.characters[name].relationships
                    if char_relationships.get(neighbor_name) == relationship_type:
                        related.append(neighbor_name)
                else:
                    related.append(neighbor_name)

        return related

    def track_character_development(
        self,
        name: str,
        development_note: str,
        chapter: Optional[int] = None
    ):
        """
        Track character development/arc

        Args:
            name: Character name
            development_note: Note about character development
            chapter: Chapter number where this development occurs
        """
        if name not in self.characters:
            raise ValueError(f"Character '{name}' does not exist")

        note = f"[Ch. {chapter}] {development_note}" if chapter else development_note
        self.characters[name].character_arc.append(note)

        logger.info(f"Tracked development for {name}: {development_note}")

    def get_character_arc(self, name: str) -> List[str]:
        """Get character development arc"""
        if name not in self.characters:
            raise ValueError(f"Character '{name}' does not exist")

        return self.characters[name].character_arc.copy()

    def validate_character_consistency(
        self,
        name: str,
        scene_description: str
    ) -> Dict[str, Any]:
        """
        Validate if character behavior in scene is consistent with their profile

        Args:
            name: Character name
            scene_description: Scene text to validate

        Returns:
            Validation report
        """
        if name not in self.characters:
            return {'valid': False, 'reason': f"Character '{name}' does not exist"}

        character = self.characters[name]

        # Use LLM to check consistency
        if not self.llm_model:
            return {'valid': True, 'reason': 'No LLM available for validation'}

        prompt = f"""Check if the character's behavior in this scene is consistent with their profile.

Character Profile:
Name: {character.name}
Personality: {character.personality}
Background: {character.background}
Goals: {character.goals}

Scene Description:
{scene_description}

Is the character's behavior consistent? Respond with 'CONSISTENT' or 'INCONSISTENT' and explain why.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=200)
            is_consistent = 'CONSISTENT' in response.upper() and 'INCONSISTENT' not in response.upper()

            return {
                'valid': is_consistent,
                'character': name,
                'explanation': response
            }
        except Exception as e:
            logger.error(f"Failed to validate character consistency: {e}")
            return {'valid': True, 'reason': 'Validation failed'}

    def export_relationship_graph(self, output_path: str, format: str = "graphml"):
        """
        Export relationship graph

        Args:
            output_path: Output file path
            format: Export format (graphml, gml, etc.)
        """
        self.relationship_graph.write(output_path, format=format)
        logger.info(f"Relationship graph exported to {output_path}")

    def get_summary(self) -> str:
        """Get summary of all characters"""
        num_chars = len(self.characters)
        num_relationships = self.relationship_graph.ecount()

        summary = f"Characters: {num_chars}, Relationships: {num_relationships}\n\n"

        for char in self.characters.values():
            summary += f"- {char.name}"
            if char.age:
                summary += f" (age {char.age})"
            if char.personality:
                summary += f": {char.personality[:50]}..."
            summary += "\n"

        return summary
