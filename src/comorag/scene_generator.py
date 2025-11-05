"""
SceneGenerator - Generates narrative scenes, dialogues, and descriptions
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SceneGenerator:
    """
    Generates scenes using LLM.

    Features:
    - Scene generation with context
    - Dialogue generation
    - Description generation
    - Style consistency
    """

    def __init__(self, llm_model, embedding_store=None, config=None):
        """
        Initialize SceneGenerator

        Args:
            llm_model: LLM for text generation
            embedding_store: Embedding store for retrieving relevant context
            config: Configuration object
        """
        self.llm_model = llm_model
        self.embedding_store = embedding_store
        self.config = config

        logger.info("SceneGenerator initialized")

    def generate_scene(
        self,
        prompt: str,
        characters: Optional[List[Dict[str, Any]]] = None,
        previous_scenes: Optional[List[str]] = None,
        tone: str = "neutral",
        style: str = "descriptive",
        pov: str = "third_person",
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a scene

        Args:
            prompt: Scene prompt/description
            characters: List of character data dictionaries
            previous_scenes: Previous scenes for context
            tone: Desired tone (mysterious, tense, lighthearted, etc.)
            style: Writing style (descriptive, concise, dialogue-heavy, etc.)
            pov: Point of view (first_person, third_person, etc.)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional generation parameters

        Returns:
            Generated scene text
        """
        # Build context from characters
        character_context = self._build_character_context(characters)

        # Build context from previous scenes
        scene_context = self._build_scene_context(previous_scenes)

        # Get style guide
        style_guide = self.config.style_guide if self.config else style

        # Construct generation prompt
        generation_prompt = self._construct_scene_prompt(
            prompt=prompt,
            character_context=character_context,
            scene_context=scene_context,
            tone=tone,
            style=style_guide,
            pov=pov
        )

        # Generate with LLM
        max_tokens = max_tokens or (self.config.max_tokens_scene if self.config else 2000)

        try:
            scene_text = self.llm_model.generate(
                generation_prompt,
                max_tokens=max_tokens,
                **kwargs
            )

            logger.info(f"Generated scene ({len(scene_text)} chars)")
            return scene_text.strip()

        except Exception as e:
            logger.error(f"Failed to generate scene: {e}")
            return f"[Scene generation failed: {e}]"

    def generate_dialogue(
        self,
        character1: Dict[str, Any],
        character2: Dict[str, Any],
        context: str,
        topic: str,
        emotion: str = "neutral",
        num_exchanges: int = 5,
        **kwargs
    ) -> str:
        """
        Generate dialogue between characters

        Args:
            character1: First character data
            character2: Second character data
            context: Scene context
            topic: Dialogue topic
            emotion: Emotional tone
            num_exchanges: Number of back-and-forth exchanges
            **kwargs: Additional generation parameters

        Returns:
            Generated dialogue
        """
        prompt = f"""Write a dialogue between {character1['name']} and {character2['name']}.

Character 1: {character1['name']}
Personality: {character1.get('personality', 'Not specified')}

Character 2: {character2['name']}
Personality: {character2.get('personality', 'Not specified')}

Context: {context}
Topic: {topic}
Emotional tone: {emotion}

Write {num_exchanges} exchanges of dialogue that feels natural and reflects each character's personality.
"""

        try:
            max_tokens = self.config.max_tokens_dialogue if self.config else 1500
            dialogue = self.llm_model.generate(prompt, max_tokens=max_tokens, **kwargs)
            logger.info(f"Generated dialogue between {character1['name']} and {character2['name']}")
            return dialogue.strip()

        except Exception as e:
            logger.error(f"Failed to generate dialogue: {e}")
            return f"[Dialogue generation failed: {e}]"

    def generate_description(
        self,
        subject: str,
        description_type: str = "setting",
        sensory_focus: Optional[List[str]] = None,
        mood: str = "neutral",
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate descriptive passage

        Args:
            subject: What to describe
            description_type: Type (setting, character_appearance, action, etc.)
            sensory_focus: Senses to emphasize (visual, auditory, tactile, etc.)
            mood: Mood to convey
            max_tokens: Maximum tokens
            **kwargs: Additional parameters

        Returns:
            Generated description
        """
        sensory_focus = sensory_focus or ["visual"]
        sensory_str = ", ".join(sensory_focus)

        prompt = f"""Write a {description_type} description of: {subject}

Focus on these senses: {sensory_str}
Mood: {mood}

Write a vivid, immersive description that brings the scene to life.
"""

        try:
            max_tokens = max_tokens or (self.config.max_tokens_description if self.config else 1000)
            description = self.llm_model.generate(prompt, max_tokens=max_tokens, **kwargs)
            logger.info(f"Generated description for '{subject}'")
            return description.strip()

        except Exception as e:
            logger.error(f"Failed to generate description: {e}")
            return f"[Description generation failed: {e}]"

    def expand_scene(
        self,
        scene_text: str,
        expansion_focus: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Expand an existing scene

        Args:
            scene_text: Original scene text
            expansion_focus: What to expand (e.g., "add more dialogue", "expand description")
            max_tokens: Maximum tokens for expansion

        Returns:
            Expanded scene text
        """
        prompt = f"""Expand the following scene.

Original scene:
{scene_text}

Expansion instructions: {expansion_focus}

Provide the expanded version that enhances the scene while maintaining consistency.
"""

        try:
            max_tokens = max_tokens or (self.config.max_tokens_scene if self.config else 2000)
            expanded = self.llm_model.generate(prompt, max_tokens=max_tokens)
            logger.info("Expanded scene")
            return expanded.strip()

        except Exception as e:
            logger.error(f"Failed to expand scene: {e}")
            return scene_text

    def refine_scene(
        self,
        scene_text: str,
        refinement_goals: List[str],
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Refine/improve an existing scene

        Args:
            scene_text: Original scene
            refinement_goals: List of improvement goals
            max_tokens: Maximum tokens

        Returns:
            Refined scene text
        """
        goals_str = "\n".join([f"- {goal}" for goal in refinement_goals])

        prompt = f"""Refine the following scene to improve it.

Original scene:
{scene_text}

Refinement goals:
{goals_str}

Provide the refined version.
"""

        try:
            max_tokens = max_tokens or (self.config.max_tokens_scene if self.config else 2000)
            refined = self.llm_model.generate(prompt, max_tokens=max_tokens)
            logger.info("Refined scene")
            return refined.strip()

        except Exception as e:
            logger.error(f"Failed to refine scene: {e}")
            return scene_text

    def _build_character_context(
        self,
        characters: Optional[List[Dict[str, Any]]]
    ) -> str:
        """Build character context string"""
        if not characters:
            return "No specific characters provided."

        context_parts = []
        for char in characters:
            char_info = [f"Name: {char['name']}"]

            if char.get('personality'):
                char_info.append(f"Personality: {char['personality']}")
            if char.get('background'):
                char_info.append(f"Background: {char['background']}")
            if char.get('goals'):
                char_info.append(f"Goals: {char['goals']}")

            context_parts.append("\n".join(char_info))

        return "\n\n".join(context_parts)

    def _build_scene_context(
        self,
        previous_scenes: Optional[List[str]]
    ) -> str:
        """Build context from previous scenes"""
        if not previous_scenes:
            return "No previous scene context."

        # Summarize previous scenes if they're too long
        context = "Previous scenes summary:\n"

        for i, scene in enumerate(previous_scenes[-3:], 1):
            # Truncate long scenes
            scene_preview = scene[:200] + "..." if len(scene) > 200 else scene
            context += f"\nScene {i}: {scene_preview}"

        return context

    def _construct_scene_prompt(
        self,
        prompt: str,
        character_context: str,
        scene_context: str,
        tone: str,
        style: str,
        pov: str
    ) -> str:
        """Construct the full scene generation prompt"""
        full_prompt = f"""You are writing a scene for a novel.

{character_context}

{scene_context}

Scene prompt: {prompt}

Writing instructions:
- Point of view: {pov}
- Tone: {tone}
- Style: {style}
- Write in a narrative prose style
- Show, don't tell
- Use vivid, sensory details
- Maintain character consistency

Write the scene now:
"""
        return full_prompt

    def generate_transition(
        self,
        from_scene: str,
        to_scene_prompt: str,
        max_tokens: int = 300
    ) -> str:
        """
        Generate a transition between scenes

        Args:
            from_scene: Previous scene (last paragraph)
            to_scene_prompt: What the next scene is about
            max_tokens: Maximum tokens

        Returns:
            Transition text
        """
        prompt = f"""Write a smooth transition between these scenes.

Previous scene ending:
{from_scene[-500:] if len(from_scene) > 500 else from_scene}

Next scene will be about: {to_scene_prompt}

Write 1-2 paragraphs that smoothly transition from the previous scene to the next.
"""

        try:
            transition = self.llm_model.generate(prompt, max_tokens=max_tokens)
            logger.info("Generated scene transition")
            return transition.strip()

        except Exception as e:
            logger.error(f"Failed to generate transition: {e}")
            return "\n\n* * *\n\n"  # Simple scene break

    def suggest_scene_improvements(
        self,
        scene_text: str
    ) -> List[str]:
        """
        Analyze scene and suggest improvements

        Args:
            scene_text: Scene to analyze

        Returns:
            List of improvement suggestions
        """
        prompt = f"""Analyze this scene and suggest 3-5 specific improvements.

Scene:
{scene_text}

Consider:
- Pacing
- Character voice
- Show vs tell
- Sensory details
- Dialogue quality

Provide concise, actionable suggestions.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=500)
            # Parse suggestions (simplified)
            suggestions = [s.strip() for s in response.split('\n') if s.strip() and len(s.strip()) > 10]
            logger.info(f"Generated {len(suggestions)} improvement suggestions")
            return suggestions

        except Exception as e:
            logger.error(f"Failed to generate suggestions: {e}")
            return []
