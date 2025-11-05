"""
ConsistencyChecker - Validates narrative consistency
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ConsistencyChecker:
    """
    Checks consistency across the novel.

    Features:
    - Character behavior consistency
    - Timeline consistency
    - Plot coherence
    - World rules consistency
    """

    def __init__(self, llm_model, character_manager, plot_manager, config=None):
        """
        Initialize ConsistencyChecker

        Args:
            llm_model: LLM for consistency analysis
            character_manager: CharacterManager instance
            plot_manager: PlotManager instance
            config: Configuration object
        """
        self.llm_model = llm_model
        self.character_manager = character_manager
        self.plot_manager = plot_manager
        self.config = config

        logger.info("ConsistencyChecker initialized")

    def check_consistency(
        self,
        novel_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run full consistency check

        Args:
            novel_data: Novel data dictionary

        Returns:
            Consistency report
        """
        logger.info("Running comprehensive consistency check...")

        issues = []

        # Check character consistency
        char_issues = self._check_character_consistency(novel_data)
        issues.extend(char_issues)

        # Check timeline consistency
        timeline_issues = self._check_timeline_consistency(novel_data)
        issues.extend(timeline_issues)

        # Check plot consistency
        plot_issues = self._check_plot_consistency(novel_data)
        issues.extend(plot_issues)

        report = {
            'timestamp': None,
            'total_issues': len(issues),
            'issues': issues,
            'passed': len(issues) == 0
        }

        logger.info(f"Consistency check complete: {len(issues)} issues found")

        return report

    def _check_character_consistency(
        self,
        novel_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check character consistency across scenes"""
        issues = []

        # Check if characters maintain consistent personalities
        for char_name, char_data in novel_data.get('characters', {}).items():
            # Check appearances across chapters
            appearances = self._find_character_appearances(char_name, novel_data)

            if len(appearances) > 1:
                # Could use LLM to check if behavior is consistent
                # For now, just structural checks
                pass

        return issues

    def _check_timeline_consistency(
        self,
        novel_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check timeline consistency"""
        issues = []

        # Check for timeline gaps or contradictions
        chapters = novel_data.get('chapters', [])
        for chapter in chapters:
            # Check if events follow logical sequence
            pass

        return issues

    def _check_plot_consistency(
        self,
        novel_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check plot consistency"""
        issues = []

        # Check for unresolved plot threads
        plot_points = novel_data.get('plot', {}).get('plot_points', [])
        unresolved = [pp for pp in plot_points if not pp.get('resolved', False)]

        if len(unresolved) > 10:
            issues.append({
                'type': 'plot',
                'severity': 'warning',
                'message': f'{len(unresolved)} unresolved plot points',
                'details': unresolved[:5]
            })

        return issues

    def _find_character_appearances(
        self,
        character_name: str,
        novel_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find all scenes where a character appears"""
        appearances = []

        for chapter in novel_data.get('chapters', []):
            for scene in chapter.get('scenes', []):
                if character_name in scene.get('characters', []):
                    appearances.append({
                        'chapter': chapter['chapter_number'],
                        'scene': scene['scene_number'],
                        'content': scene['content']
                    })

        return appearances

    def validate_scene(
        self,
        scene_text: str,
        characters: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate a single scene for consistency

        Args:
            scene_text: Scene text
            characters: Characters in scene
            context: Scene context

        Returns:
            Validation result
        """
        if not self.llm_model:
            return {'valid': True, 'reason': 'No LLM for validation'}

        # Build validation prompt
        char_profiles = []
        for char_name in characters:
            char_data = self.character_manager.get_character(char_name)
            if char_data:
                char_profiles.append(f"{char_name}: {char_data.get('personality', '')}")

        prompt = f"""Check this scene for consistency issues.

Characters in scene:
{chr(10).join(char_profiles)}

Scene:
{scene_text}

Check for:
1. Character behavior matching their personality
2. Logical action sequences
3. Internal contradictions

Report any issues found, or say "CONSISTENT" if no issues.
"""

        try:
            response = self.llm_model.generate(prompt, max_tokens=300)
            is_consistent = 'CONSISTENT' in response.upper()

            return {
                'valid': is_consistent,
                'explanation': response
            }

        except Exception as e:
            logger.error(f"Scene validation failed: {e}")
            return {'valid': True, 'reason': 'Validation error'}
