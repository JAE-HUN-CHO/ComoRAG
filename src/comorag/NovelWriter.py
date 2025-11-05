"""
NovelWriter - Main class for AI-powered long-form novel writing
"""
import json
import os
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Union, Optional, List, Dict, Any, Tuple
from tqdm import tqdm
import igraph as ig

from .llm import _get_llm_class, BaseLLM
from .embedding_model import _get_embedding_model_class, BaseEmbeddingModel
from .embedding_store import EmbeddingStore
from .utils.config_utils import BaseConfig
from .character_manager import CharacterManager
from .plot_manager import PlotManager
from .scene_generator import SceneGenerator
from .consistency_checker import ConsistencyChecker
from .world_builder import WorldBuilder

logger = logging.getLogger(__name__)


@dataclass
class NovelConfig(BaseConfig):
    """Configuration for Novel Writing"""
    novel_title: str = "Untitled Novel"
    genre: str = "general"
    style_guide: str = "descriptive, engaging"

    # Token limits for different generation tasks
    max_tokens_scene: int = 2000
    max_tokens_dialogue: int = 1500
    max_tokens_description: int = 1000

    # Consistency checking
    consistency_check: bool = True
    auto_save: bool = True

    # Output settings
    output_format: str = "markdown"  # markdown, json, txt


class NovelWriter:
    """
    Main class for AI-powered novel writing.

    Manages:
    - Character creation and tracking
    - Plot structure and timeline
    - Scene generation
    - Consistency validation
    - World building
    """

    def __init__(
        self,
        config: Optional[NovelConfig] = None,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        llm_model_name: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_api_key: Optional[str] = None,
        embedding_model_name: Optional[str] = None,
    ):
        """
        Initialize NovelWriter

        Args:
            config: NovelConfig object with all settings
            title: Novel title (overrides config)
            genre: Novel genre (overrides config)
            llm_model_name: LLM model to use
            llm_base_url: Base URL for LLM API
            llm_api_key: API key for LLM
            embedding_model_name: Embedding model for semantic search
        """
        # Setup configuration
        if config is None:
            self.config = NovelConfig()
        else:
            self.config = config

        if title is not None:
            self.config.novel_title = title
        if genre is not None:
            self.config.genre = genre
        if llm_model_name is not None:
            self.config.llm_name = llm_model_name
        if llm_base_url is not None:
            self.config.llm_base_url = llm_base_url
        if llm_api_key is not None:
            self.config.llm_api_key = llm_api_key
        if embedding_model_name is not None:
            self.config.embedding_model_name = embedding_model_name

        logger.info(f"Initializing NovelWriter for '{self.config.novel_title}'")
        logger.debug(f"Genre: {self.config.genre}, Style: {self.config.style_guide}")

        # Setup working directory
        self.working_dir = os.path.join(
            self.config.save_dir or "novels",
            self._sanitize_filename(self.config.novel_title)
        )
        os.makedirs(self.working_dir, exist_ok=True)
        logger.info(f"Working directory: {self.working_dir}")

        # Initialize LLM
        self.llm_model: BaseLLM = _get_llm_class(self.config)
        logger.info(f"LLM initialized: {self.config.llm_name}")

        # Initialize embedding model for semantic search
        if embedding_model_name:
            self.embedding_model: BaseEmbeddingModel = _get_embedding_model_class(
                embedding_model_name=self.config.embedding_model_name
            )(
                global_config=self.config,
                embedding_model_name=self.config.embedding_model_name
            )

            # Embedding stores for different content types
            self.scene_embedding_store = EmbeddingStore(
                self.embedding_model,
                os.path.join(self.working_dir, "scene_embeddings"),
                self.config.embedding_batch_size,
                'scene'
            )
            self.character_embedding_store = EmbeddingStore(
                self.embedding_model,
                os.path.join(self.working_dir, "character_embeddings"),
                self.config.embedding_batch_size,
                'character'
            )
        else:
            self.embedding_model = None
            self.scene_embedding_store = None
            self.character_embedding_store = None

        # Initialize core modules
        self.character_manager = CharacterManager(
            llm_model=self.llm_model,
            embedding_store=self.character_embedding_store,
            config=self.config
        )

        self.plot_manager = PlotManager(
            llm_model=self.llm_model,
            config=self.config
        )

        self.scene_generator = SceneGenerator(
            llm_model=self.llm_model,
            embedding_store=self.scene_embedding_store,
            config=self.config
        )

        self.consistency_checker = ConsistencyChecker(
            llm_model=self.llm_model,
            character_manager=self.character_manager,
            plot_manager=self.plot_manager,
            config=self.config
        )

        self.world_builder = WorldBuilder(
            llm_model=self.llm_model,
            config=self.config
        )

        # Novel data structure
        self.novel_data = {
            "title": self.config.novel_title,
            "genre": self.config.genre,
            "style": self.config.style_guide,
            "created_at": datetime.now().isoformat(),
            "characters": {},
            "plot": {},
            "world": {},
            "chapters": []
        }

        # Load existing project if available
        self._load_project()

        logger.info("NovelWriter initialization complete")

    def _sanitize_filename(self, name: str) -> str:
        """Convert title to safe filename"""
        return "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()

    def _load_project(self):
        """Load existing novel project if it exists"""
        project_file = os.path.join(self.working_dir, "novel_project.json")
        if os.path.exists(project_file):
            logger.info(f"Loading existing project from {project_file}")
            with open(project_file, 'r', encoding='utf-8') as f:
                self.novel_data = json.load(f)
                logger.info(f"Loaded project with {len(self.novel_data.get('chapters', []))} chapters")

    def save_project(self):
        """Save current novel project"""
        project_file = os.path.join(self.working_dir, "novel_project.json")
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(self.novel_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Project saved to {project_file}")

    def create_character(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new character

        Args:
            name: Character name
            **kwargs: Additional character attributes (age, personality, background, etc.)

        Returns:
            Character data dictionary
        """
        character = self.character_manager.create_character(name, **kwargs)
        self.novel_data['characters'][name] = character

        if self.config.auto_save:
            self.save_project()

        logger.info(f"Created character: {name}")
        return character

    def add_plot_point(self, chapter: int, event: str, **kwargs):
        """
        Add a plot point

        Args:
            chapter: Chapter number
            event: Event description
            **kwargs: Additional plot point attributes
        """
        self.plot_manager.add_plot_point(chapter, event, **kwargs)

        # Update novel data
        if 'plot_points' not in self.novel_data['plot']:
            self.novel_data['plot']['plot_points'] = []

        self.novel_data['plot']['plot_points'].append({
            'chapter': chapter,
            'event': event,
            **kwargs
        })

        if self.config.auto_save:
            self.save_project()

        logger.info(f"Added plot point to chapter {chapter}: {event}")

    def generate_scene(
        self,
        chapter: int,
        scene_number: int,
        prompt: str,
        characters: Optional[List[str]] = None,
        tone: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a scene

        Args:
            chapter: Chapter number
            scene_number: Scene number within chapter
            prompt: Scene description/prompt
            characters: List of character names in this scene
            tone: Desired tone for the scene
            **kwargs: Additional generation parameters

        Returns:
            Generated scene text
        """
        logger.info(f"Generating scene {chapter}.{scene_number}")

        # Get character context
        character_context = []
        if characters:
            for char_name in characters:
                char_data = self.novel_data['characters'].get(char_name)
                if char_data:
                    character_context.append(char_data)

        # Get previous scenes for context
        previous_scenes = self._get_previous_scenes(chapter, scene_number, limit=3)

        # Generate scene
        scene_text = self.scene_generator.generate_scene(
            prompt=prompt,
            characters=character_context,
            previous_scenes=previous_scenes,
            tone=tone or self.config.style_guide,
            **kwargs
        )

        # Store scene
        self._store_scene(chapter, scene_number, scene_text, prompt, characters)

        if self.config.auto_save:
            self.save_project()

        return scene_text

    def _get_previous_scenes(self, chapter: int, scene_number: int, limit: int = 3) -> List[str]:
        """Get previous scenes for context"""
        scenes = []

        for chap in self.novel_data.get('chapters', []):
            if chap['chapter_number'] < chapter or \
               (chap['chapter_number'] == chapter and chap.get('scenes', [])):
                for scene in chap.get('scenes', []):
                    if chap['chapter_number'] == chapter and scene['scene_number'] >= scene_number:
                        break
                    scenes.append(scene['content'])

        return scenes[-limit:] if scenes else []

    def _store_scene(self, chapter: int, scene_number: int, content: str,
                     prompt: str, characters: Optional[List[str]]):
        """Store generated scene"""
        # Find or create chapter
        chapter_obj = None
        for chap in self.novel_data['chapters']:
            if chap['chapter_number'] == chapter:
                chapter_obj = chap
                break

        if not chapter_obj:
            chapter_obj = {
                'chapter_number': chapter,
                'scenes': []
            }
            self.novel_data['chapters'].append(chapter_obj)

        # Add scene
        scene_obj = {
            'scene_number': scene_number,
            'prompt': prompt,
            'content': content,
            'characters': characters or [],
            'created_at': datetime.now().isoformat()
        }
        chapter_obj['scenes'].append(scene_obj)

    def check_consistency(self) -> Dict[str, Any]:
        """
        Check narrative consistency

        Returns:
            Consistency report dictionary
        """
        logger.info("Running consistency check...")

        report = self.consistency_checker.check_consistency(
            novel_data=self.novel_data
        )

        logger.info(f"Consistency check complete. Issues found: {len(report.get('issues', []))}")

        return report

    def export(self, format: str = "markdown", output_path: Optional[str] = None) -> str:
        """
        Export novel to file

        Args:
            format: Export format (markdown, json, txt)
            output_path: Output file path (auto-generated if not provided)

        Returns:
            Path to exported file
        """
        if output_path is None:
            output_path = os.path.join(
                self.working_dir,
                f"{self._sanitize_filename(self.config.novel_title)}.{format}"
            )

        if format == "markdown":
            self._export_markdown(output_path)
        elif format == "json":
            self._export_json(output_path)
        elif format == "txt":
            self._export_txt(output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        logger.info(f"Novel exported to {output_path}")
        return output_path

    def _export_markdown(self, output_path: str):
        """Export as Markdown"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.novel_data['title']}\n\n")
            f.write(f"**Genre**: {self.novel_data['genre']}\n\n")
            f.write(f"---\n\n")

            for chapter in sorted(self.novel_data.get('chapters', []),
                                 key=lambda x: x['chapter_number']):
                f.write(f"## Chapter {chapter['chapter_number']}\n\n")

                for scene in sorted(chapter.get('scenes', []),
                                   key=lambda x: x['scene_number']):
                    f.write(f"{scene['content']}\n\n")
                    f.write("---\n\n")

    def _export_json(self, output_path: str):
        """Export as JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.novel_data, f, indent=2, ensure_ascii=False)

    def _export_txt(self, output_path: str):
        """Export as plain text"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{self.novel_data['title']}\n")
            f.write(f"{'=' * len(self.novel_data['title'])}\n\n")

            for chapter in sorted(self.novel_data.get('chapters', []),
                                 key=lambda x: x['chapter_number']):
                f.write(f"Chapter {chapter['chapter_number']}\n\n")

                for scene in sorted(chapter.get('scenes', []),
                                   key=lambda x: x['scene_number']):
                    f.write(f"{scene['content']}\n\n")

    def get_summary(self) -> str:
        """Get a summary of the novel project"""
        num_chapters = len(self.novel_data.get('chapters', []))
        num_scenes = sum(len(chap.get('scenes', []))
                        for chap in self.novel_data.get('chapters', []))
        num_characters = len(self.novel_data.get('characters', {}))

        summary = f"""
Novel Project Summary:
----------------------
Title: {self.novel_data['title']}
Genre: {self.novel_data['genre']}
Characters: {num_characters}
Chapters: {num_chapters}
Scenes: {num_scenes}
Working Directory: {self.working_dir}
        """
        return summary.strip()
