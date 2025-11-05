"""
PlotManager - Manages plot structure, timeline, and story progression
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class PlotImportance(Enum):
    """Plot point importance levels"""
    CRITICAL = "critical"  # Main plot points
    MAJOR = "major"  # Important developments
    MINOR = "minor"  # Supporting events
    BACKGROUND = "background"  # World-building, atmosphere


@dataclass
class PlotPoint:
    """Represents a plot point in the story"""
    chapter: int
    event: str
    importance: PlotImportance = PlotImportance.MINOR
    characters_involved: List[str] = field(default_factory=list)
    location: str = ""
    consequences: List[str] = field(default_factory=list)
    foreshadowing: List[str] = field(default_factory=list)
    resolved: bool = False
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'chapter': self.chapter,
            'event': self.event,
            'importance': self.importance.value,
            'characters_involved': self.characters_involved,
            'location': self.location,
            'consequences': self.consequences,
            'foreshadowing': self.foreshadowing,
            'resolved': self.resolved,
            'notes': self.notes,
            'created_at': self.created_at
        }


@dataclass
class Chapter:
    """Represents a chapter in the novel"""
    number: int
    title: str = ""
    summary: str = ""
    plot_points: List[PlotPoint] = field(default_factory=list)
    characters: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    word_count: int = 0
    status: str = "planned"  # planned, outlined, drafted, revised, complete

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'number': self.number,
            'title': self.title,
            'summary': self.summary,
            'plot_points': [pp.to_dict() for pp in self.plot_points],
            'characters': self.characters,
            'locations': self.locations,
            'word_count': self.word_count,
            'status': self.status
        }


class PlotManager:
    """
    Manages plot structure and timeline.

    Features:
    - Chapter organization
    - Plot point tracking
    - Timeline management
    - Foreshadowing and payoff tracking
    - Plot consistency checking
    """

    def __init__(self, llm_model, config=None):
        """
        Initialize PlotManager

        Args:
            llm_model: LLM for generating plot suggestions
            config: Configuration object
        """
        self.llm_model = llm_model
        self.config = config

        # Storage
        self.chapters: Dict[int, Chapter] = {}
        self.plot_points: List[PlotPoint] = []
        self.timeline: List[Dict[str, Any]] = []

        # Story structure
        self.story_structure = {
            'exposition': [],
            'rising_action': [],
            'climax': [],
            'falling_action': [],
            'resolution': []
        }

        logger.info("PlotManager initialized")

    def create_chapter(
        self,
        number: int,
        title: str = "",
        summary: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new chapter

        Args:
            number: Chapter number
            title: Chapter title
            summary: Chapter summary
            **kwargs: Additional chapter attributes

        Returns:
            Chapter data dictionary
        """
        if number in self.chapters:
            logger.warning(f"Chapter {number} already exists. Use update_chapter instead.")
            return self.chapters[number].to_dict()

        chapter = Chapter(
            number=number,
            title=title,
            summary=summary,
            **kwargs
        )

        self.chapters[number] = chapter
        logger.info(f"Created chapter {number}: {title}")

        return chapter.to_dict()

    def update_chapter(
        self,
        number: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update existing chapter

        Args:
            number: Chapter number
            **kwargs: Attributes to update

        Returns:
            Updated chapter data
        """
        if number not in self.chapters:
            logger.warning(f"Chapter {number} doesn't exist. Creating it.")
            return self.create_chapter(number, **kwargs)

        chapter = self.chapters[number]

        for key, value in kwargs.items():
            if hasattr(chapter, key) and value is not None:
                setattr(chapter, key, value)

        logger.info(f"Updated chapter {number}")

        return chapter.to_dict()

    def add_plot_point(
        self,
        chapter: int,
        event: str,
        importance: str = "minor",
        characters_involved: Optional[List[str]] = None,
        location: str = "",
        consequences: Optional[List[str]] = None,
        foreshadowing: Optional[List[str]] = None,
        **kwargs
    ) -> PlotPoint:
        """
        Add a plot point

        Args:
            chapter: Chapter number
            event: Event description
            importance: Importance level (critical, major, minor, background)
            characters_involved: List of character names
            location: Where the event occurs
            consequences: List of consequences
            foreshadowing: What this foreshadows
            **kwargs: Additional plot point attributes

        Returns:
            PlotPoint object
        """
        # Create chapter if it doesn't exist
        if chapter not in self.chapters:
            self.create_chapter(chapter)

        # Parse importance
        try:
            importance_enum = PlotImportance(importance.lower())
        except ValueError:
            importance_enum = PlotImportance.MINOR
            logger.warning(f"Invalid importance '{importance}', using MINOR")

        plot_point = PlotPoint(
            chapter=chapter,
            event=event,
            importance=importance_enum,
            characters_involved=characters_involved or [],
            location=location,
            consequences=consequences or [],
            foreshadowing=foreshadowing or [],
            notes=kwargs.get('notes', '')
        )

        self.plot_points.append(plot_point)
        self.chapters[chapter].plot_points.append(plot_point)

        logger.info(f"Added plot point to chapter {chapter}: {event}")

        return plot_point

    def get_chapter(self, number: int) -> Optional[Dict[str, Any]]:
        """Get chapter by number"""
        chapter = self.chapters.get(number)
        return chapter.to_dict() if chapter else None

    def get_all_chapters(self) -> List[Dict[str, Any]]:
        """Get all chapters"""
        return [
            self.chapters[num].to_dict()
            for num in sorted(self.chapters.keys())
        ]

    def get_plot_points(
        self,
        chapter: Optional[int] = None,
        importance: Optional[str] = None,
        resolved: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get plot points with optional filtering

        Args:
            chapter: Filter by chapter number
            importance: Filter by importance level
            resolved: Filter by resolved status

        Returns:
            List of plot point dictionaries
        """
        filtered = self.plot_points

        if chapter is not None:
            filtered = [pp for pp in filtered if pp.chapter == chapter]

        if importance is not None:
            importance_enum = PlotImportance(importance.lower())
            filtered = [pp for pp in filtered if pp.importance == importance_enum]

        if resolved is not None:
            filtered = [pp for pp in filtered if pp.resolved == resolved]

        return [pp.to_dict() for pp in filtered]

    def resolve_plot_point(self, chapter: int, event: str):
        """
        Mark a plot point as resolved

        Args:
            chapter: Chapter number
            event: Event description (partial match)
        """
        for plot_point in self.plot_points:
            if plot_point.chapter == chapter and event.lower() in plot_point.event.lower():
                plot_point.resolved = True
                logger.info(f"Resolved plot point: {plot_point.event}")
                return

        logger.warning(f"Plot point not found: chapter {chapter}, event '{event}'")

    def add_foreshadowing(
        self,
        from_chapter: int,
        from_event: str,
        foreshadows: str
    ):
        """
        Add foreshadowing to a plot point

        Args:
            from_chapter: Chapter where foreshadowing occurs
            from_event: Event that does the foreshadowing
            foreshadows: What it foreshadows
        """
        for plot_point in self.plot_points:
            if plot_point.chapter == from_chapter and from_event.lower() in plot_point.event.lower():
                plot_point.foreshadowing.append(foreshadows)
                logger.info(f"Added foreshadowing: {from_event} -> {foreshadows}")
                return

        logger.warning(f"Plot point not found for foreshadowing: {from_event}")

    def generate_plot_outline(
        self,
        premise: str,
        num_chapters: int = 20,
        genre: str = "general"
    ) -> List[Dict[str, Any]]:
        """
        Use LLM to generate a plot outline

        Args:
            premise: Story premise
            num_chapters: Number of chapters
            genre: Story genre

        Returns:
            List of chapter outlines
        """
        if not self.llm_model:
            logger.error("No LLM available for plot generation")
            return []

        prompt = f"""Create a {num_chapters}-chapter outline for a {genre} novel.

Premise: {premise}

For each chapter, provide:
1. Chapter title
2. Brief summary (2-3 sentences)
3. Key plot points
4. Characters involved

Format as a structured outline.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=2000)
            logger.info("Generated plot outline with LLM")

            # Parse response and create chapters (simplified)
            # In production, would parse more carefully
            return [{'outline': response}]

        except Exception as e:
            logger.error(f"Failed to generate plot outline: {e}")
            return []

    def suggest_next_plot_point(
        self,
        current_chapter: int
    ) -> Optional[str]:
        """
        Suggest the next plot point based on story so far

        Args:
            current_chapter: Current chapter number

        Returns:
            Suggested plot point description
        """
        if not self.llm_model:
            return None

        # Get recent plot points
        recent_points = [
            pp for pp in self.plot_points
            if pp.chapter <= current_chapter
        ][-5:]

        recent_summary = "\n".join([
            f"Ch. {pp.chapter}: {pp.event}"
            for pp in recent_points
        ])

        # Get unresolved plot points
        unresolved = [
            pp for pp in self.plot_points
            if not pp.resolved and pp.chapter <= current_chapter
        ]

        unresolved_summary = "\n".join([
            f"- {pp.event}"
            for pp in unresolved[:5]
        ])

        prompt = f"""Based on the story so far, suggest the next plot development for chapter {current_chapter + 1}.

Recent plot points:
{recent_summary}

Unresolved plot points:
{unresolved_summary}

Suggest a logical next plot point that:
1. Advances the story
2. Addresses or develops unresolved threads
3. Maintains narrative tension

Provide a brief 1-2 sentence suggestion.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=150)
            logger.info(f"Generated plot suggestion: {response[:100]}...")
            return response.strip()

        except Exception as e:
            logger.error(f"Failed to generate plot suggestion: {e}")
            return None

    def analyze_pacing(self) -> Dict[str, Any]:
        """
        Analyze story pacing

        Returns:
            Pacing analysis report
        """
        if not self.plot_points:
            return {'status': 'No plot points to analyze'}

        # Count plot points by importance per chapter
        chapter_intensity = {}

        for pp in self.plot_points:
            if pp.chapter not in chapter_intensity:
                chapter_intensity[pp.chapter] = {
                    'critical': 0,
                    'major': 0,
                    'minor': 0,
                    'background': 0
                }
            chapter_intensity[pp.chapter][pp.importance.value] += 1

        # Identify pacing issues
        issues = []

        for chapter, intensity in chapter_intensity.items():
            total = sum(intensity.values())

            # Check for overloaded chapters
            if intensity['critical'] > 2:
                issues.append(f"Chapter {chapter}: Too many critical events ({intensity['critical']})")

            # Check for empty chapters
            if total == 0:
                issues.append(f"Chapter {chapter}: No plot points")

        return {
            'chapter_intensity': chapter_intensity,
            'issues': issues,
            'total_plot_points': len(self.plot_points),
            'unresolved_plot_points': sum(1 for pp in self.plot_points if not pp.resolved)
        }

    def get_timeline(self) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of all plot points

        Returns:
            Sorted list of plot points
        """
        sorted_points = sorted(self.plot_points, key=lambda x: x.chapter)
        return [pp.to_dict() for pp in sorted_points]

    def export_outline(self, format: str = "markdown") -> str:
        """
        Export plot outline

        Args:
            format: Export format (markdown, json)

        Returns:
            Formatted outline string
        """
        if format == "markdown":
            outline = "# Plot Outline\n\n"

            for chapter_num in sorted(self.chapters.keys()):
                chapter = self.chapters[chapter_num]
                outline += f"## Chapter {chapter.number}"

                if chapter.title:
                    outline += f": {chapter.title}"
                outline += "\n\n"

                if chapter.summary:
                    outline += f"_{chapter.summary}_\n\n"

                if chapter.plot_points:
                    outline += "**Plot Points:**\n"
                    for pp in chapter.plot_points:
                        outline += f"- [{pp.importance.value.upper()}] {pp.event}\n"
                    outline += "\n"

            return outline

        elif format == "json":
            import json
            return json.dumps(self.get_all_chapters(), indent=2)

        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_summary(self) -> str:
        """Get summary of plot structure"""
        num_chapters = len(self.chapters)
        num_plot_points = len(self.plot_points)
        num_unresolved = sum(1 for pp in self.plot_points if not pp.resolved)

        critical_points = sum(1 for pp in self.plot_points
                            if pp.importance == PlotImportance.CRITICAL)

        return f"""
Plot Structure Summary:
----------------------
Chapters: {num_chapters}
Plot Points: {num_plot_points}
  - Critical: {critical_points}
  - Unresolved: {num_unresolved}
        """.strip()
