"""
Prompt templates for scene generation
"""

SCENE_GENERATION_TEMPLATE = """You are a skilled novelist writing a scene for a {genre} novel.

CHARACTERS IN SCENE:
{character_context}

PREVIOUS CONTEXT:
{scene_context}

SCENE PROMPT: {prompt}

WRITING GUIDELINES:
- Point of view: {pov}
- Tone: {tone}
- Style: {style}
- Use vivid, sensory details
- Show emotions through actions and dialogue
- Maintain character consistency
- Create engaging, immersive prose

Write the scene now:
"""

DIALOGUE_GENERATION_TEMPLATE = """Write a dialogue between {char1_name} and {char2_name}.

CHARACTER 1: {char1_name}
Personality: {char1_personality}
Current mood: {char1_mood}

CHARACTER 2: {char2_name}
Personality: {char2_personality}
Current mood: {char2_mood}

CONTEXT: {context}
TOPIC: {topic}

Write {num_exchanges} exchanges of natural, character-appropriate dialogue.
"""

DESCRIPTION_TEMPLATE = """Write a {description_type} description.

SUBJECT: {subject}
SENSORY FOCUS: {sensory_focus}
MOOD/ATMOSPHERE: {mood}

Create a vivid, immersive description that brings this to life for the reader.
"""

CHARACTER_EXPANSION_TEMPLATE = """Expand this character profile with rich, consistent details.

CHARACTER: {name}
Current details:
{current_details}

Provide:
1. Enhanced personality traits
2. Deeper background story
3. Physical appearance
4. Motivations and goals
5. Fears and vulnerabilities
6. Unique mannerisms or quirks

Keep it concise but vivid and memorable.
"""

PLOT_OUTLINE_TEMPLATE = """Create a {num_chapters}-chapter outline for a {genre} novel.

PREMISE: {premise}

For each chapter, provide:
1. Chapter title
2. Brief summary (2-3 sentences)
3. Key plot points
4. Main characters involved
5. Emotional arc

Structure the outline with clear rising action, climax, and resolution.
"""

PLOT_SUGGESTION_TEMPLATE = """Suggest the next plot development for chapter {next_chapter}.

RECENT EVENTS:
{recent_events}

UNRESOLVED PLOT THREADS:
{unresolved_threads}

Suggest a logical next plot point that:
1. Advances the story
2. Develops unresolved threads
3. Maintains narrative tension
4. Feels organic to the story

Provide a brief 1-2 sentence suggestion.
"""

CONSISTENCY_CHECK_TEMPLATE = """Check this scene for consistency issues.

CHARACTER PROFILES:
{character_profiles}

ESTABLISHED WORLD RULES:
{world_rules}

SCENE TO CHECK:
{scene_text}

Check for:
1. Character behavior matching their personality
2. Adherence to world rules
3. Logical action sequences
4. Timeline consistency
5. Internal contradictions

Report specific issues found, or respond "CONSISTENT" if no issues detected.
"""

SCENE_REFINEMENT_TEMPLATE = """Refine and improve the following scene.

ORIGINAL SCENE:
{scene_text}

REFINEMENT GOALS:
{refinement_goals}

GENRE: {genre}
STYLE: {style}

Provide the refined version that addresses the goals while maintaining the scene's core essence.
"""

TRANSITION_TEMPLATE = """Write a smooth transition between these two scenes.

PREVIOUS SCENE ENDING:
{previous_scene}

NEXT SCENE WILL COVER:
{next_scene_summary}

Write 1-2 paragraphs that naturally bridge these scenes.
"""

LOCATION_DESCRIPTION_TEMPLATE = """Describe this location in vivid detail.

LOCATION: {location_name}
TYPE: {location_type}
MOOD: {mood}
TIME OF DAY: {time_of_day}

Include:
- Visual details (architecture, landscape, lighting)
- Sounds
- Smells
- Atmosphere and feeling
- Notable or unique features

Create an immersive description that makes the reader feel present.
"""
