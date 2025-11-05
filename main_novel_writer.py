"""
NovelForge - AI-Powered Novel Writing Framework
Main example script demonstrating novel creation
"""
import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.comorag.NovelWriter import NovelWriter, NovelConfig
from src.comorag.utils.logging_utils import setup_logger

# Setup logging
logger = setup_logger(
    name="NovelForge",
    log_file="novelforge.log",
    level=logging.INFO
)


def create_fantasy_novel_example():
    """Example: Creating a fantasy novel"""

    # Configure NovelWriter
    config = NovelConfig(
        llm_base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        llm_api_key=os.getenv('OPENAI_API_KEY', 'your-api-key-here'),
        llm_name='gpt-4o-mini',  # or gpt-4o for better quality
        novel_title='The Last Sage',
        genre='fantasy',
        style_guide='descriptive, immersive, with vivid imagery',
        embedding_model_name=None,  # Optional: add for semantic search
        output_dir='novels',
        max_tokens_scene=2000,
        max_tokens_dialogue=1500,
        consistency_check=True,
        auto_save=True
    )

    # Initialize NovelWriter
    logger.info("Initializing NovelWriter...")
    novel = NovelWriter(config=config)

    logger.info("=== Creating Characters ===")

    # Create protagonist
    aria = novel.create_character(
        name="Aria Windwhisper",
        age=24,
        gender="female",
        personality="determined, curious, empathetic but haunted by past failures",
        background="Last surviving sage of the Windwhisper lineage. "
                  "Watched her mentor die protecting an ancient secret. "
                  "Now seeks to prevent the return of the Shadow King.",
        appearance="Silver-white hair, piercing blue eyes that glow faintly when using magic. "
                  "Wears the traditional azure robes of a sage.",
        goals="Master the forbidden seventh seal to stop the Shadow King's resurrection",
        fears="Failing again, losing those she cares about, becoming corrupted by dark magic",
        first_appearance=1
    )

    # Create supporting character
    kael = novel.create_character(
        name="Kael Ironheart",
        age=28,
        gender="male",
        personality="brave, loyal, pragmatic with a dry sense of humor",
        background="Former royal guard who deserted when he learned of the king's dark pact. "
                  "Now a wandering mercenary seeking redemption.",
        appearance="Scarred face, muscular build, short dark hair, always wears his old guard medallion",
        goals="Protect Aria and atone for his failure to stop the corruption of the kingdom",
        fears="Being too late to make a difference, losing his honor completely",
        first_appearance=1
    )

    # Create antagonist
    shadowking = novel.create_character(
        name="The Shadow King",
        age=None,
        gender="male",
        personality="manipulative, patient, power-hungry, sees mortals as pawns",
        background="Ancient sorcerer who sought immortality through dark magic. "
                  "Was sealed away by the Seven Sages centuries ago. "
                  "Now his followers seek to resurrect him.",
        goals="Return to the mortal realm and conquer all kingdoms",
        fears="Being sealed away again, the power of the Seven Seals",
        first_appearance=3
    )

    # Add relationships
    novel.character_manager.add_relationship(
        "Aria Windwhisper",
        "Kael Ironheart",
        "ally",
        "Reluctant allies who develop deep trust"
    )

    logger.info("=== Creating Plot Structure ===")

    # Define key plot points
    novel.add_plot_point(
        chapter=1,
        event="Aria discovers her mentor's hidden journal revealing the truth about the Seven Seals",
        importance="critical",
        characters_involved=["Aria Windwhisper"],
        location="Abandoned Sage Tower"
    )

    novel.add_plot_point(
        chapter=1,
        event="Aria is attacked by Shadow cultists seeking the journal",
        importance="major",
        characters_involved=["Aria Windwhisper", "Kael Ironheart"]
    )

    novel.add_plot_point(
        chapter=2,
        event="Aria and Kael journey to the first seal location in the Whispering Woods",
        importance="major",
        characters_involved=["Aria Windwhisper", "Kael Ironheart"]
    )

    novel.add_plot_point(
        chapter=3,
        event="They discover the first seal has been weakened by the cultists",
        importance="critical",
        characters_involved=["Aria Windwhisper", "Kael Ironheart"]
    )

    logger.info("=== Generating Opening Scene ===")

    # Generate opening scene
    scene1 = novel.generate_scene(
        chapter=1,
        scene_number=1,
        prompt="Aria explores her deceased mentor's tower at night, "
              "searching for clues. She discovers a hidden compartment "
              "containing a journal. As she reads the shocking truth about "
              "the Seven Seals, she hears footsteps approaching.",
        characters=["Aria Windwhisper"],
        tone="mysterious, tense, with growing dread"
    )

    print("\n" + "="*60)
    print("GENERATED OPENING SCENE:")
    print("="*60)
    print(scene1)
    print("="*60 + "\n")

    # Generate second scene
    logger.info("=== Generating Action Scene ===")

    scene2 = novel.generate_scene(
        chapter=1,
        scene_number=2,
        prompt="Shadow cultists burst into the tower. Aria fights them off "
              "using her sage magic, but she's outnumbered. Just as they're "
              "about to overwhelm her, Kael Ironheart crashes through a window, "
              "joining the fight. Together they barely escape.",
        characters=["Aria Windwhisper", "Kael Ironheart"],
        tone="intense, action-packed, desperate"
    )

    print("\n" + "="*60)
    print("GENERATED ACTION SCENE:")
    print("="*60)
    print(scene2)
    print("="*60 + "\n")

    # Check consistency
    if config.consistency_check:
        logger.info("=== Running Consistency Check ===")
        report = novel.check_consistency()
        print(f"\nConsistency Check: {report['total_issues']} issues found")
        if report['issues']:
            for issue in report['issues']:
                print(f"  - [{issue['type']}] {issue['message']}")

    # Save project
    logger.info("=== Saving Project ===")
    novel.save_project()

    # Export novel
    logger.info("=== Exporting Novel ===")
    markdown_path = novel.export(format="markdown")
    json_path = novel.export(format="json")

    print(f"\n✅ Novel exported to:")
    print(f"   - {markdown_path}")
    print(f"   - {json_path}")

    # Print summary
    print("\n" + "="*60)
    print(novel.get_summary())
    print("="*60)

    return novel


def interactive_mode():
    """Interactive novel creation mode"""
    print("\n" + "="*60)
    print("NovelForge - Interactive Novel Creation")
    print("="*60 + "\n")

    # Get basic info
    title = input("Enter novel title: ").strip()
    genre = input("Enter genre (fantasy/sci-fi/mystery/romance/etc): ").strip() or "general"

    # Configure
    config = NovelConfig(
        llm_base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        llm_api_key=os.getenv('OPENAI_API_KEY', 'your-api-key-here'),
        llm_name='gpt-4o-mini',
        novel_title=title,
        genre=genre,
        output_dir='novels',
        auto_save=True
    )

    novel = NovelWriter(config=config)

    print(f"\n✅ Created novel project: {title}")
    print(f"📁 Working directory: {novel.working_dir}\n")

    # Interactive menu
    while True:
        print("\nWhat would you like to do?")
        print("1. Create a character")
        print("2. Add a plot point")
        print("3. Generate a scene")
        print("4. Check consistency")
        print("5. Export novel")
        print("6. View summary")
        print("7. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            name = input("Character name: ").strip()
            personality = input("Personality: ").strip()
            background = input("Background: ").strip()

            novel.create_character(
                name=name,
                personality=personality,
                background=background
            )
            print(f"✅ Created character: {name}")

        elif choice == "2":
            chapter = int(input("Chapter number: ").strip())
            event = input("Plot event description: ").strip()
            importance = input("Importance (critical/major/minor): ").strip() or "minor"

            novel.add_plot_point(
                chapter=chapter,
                event=event,
                importance=importance
            )
            print(f"✅ Added plot point to chapter {chapter}")

        elif choice == "3":
            chapter = int(input("Chapter number: ").strip())
            scene_num = int(input("Scene number: ").strip())
            prompt = input("Scene description: ").strip()

            print("\n⏳ Generating scene...")
            scene = novel.generate_scene(
                chapter=chapter,
                scene_number=scene_num,
                prompt=prompt
            )

            print("\n" + "="*60)
            print("GENERATED SCENE:")
            print("="*60)
            print(scene)
            print("="*60)

        elif choice == "4":
            print("\n⏳ Running consistency check...")
            report = novel.check_consistency()
            print(f"\n✅ Check complete: {report['total_issues']} issues found")

        elif choice == "5":
            format_choice = input("Format (markdown/json/txt): ").strip() or "markdown"
            path = novel.export(format=format_choice)
            print(f"✅ Exported to: {path}")

        elif choice == "6":
            print(novel.get_summary())

        elif choice == "7":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="NovelForge - AI-Powered Novel Writing Framework"
    )
    parser.add_argument(
        '--mode',
        choices=['example', 'interactive'],
        default='example',
        help='Run mode: example (demo) or interactive'
    )

    args = parser.parse_args()

    try:
        if args.mode == 'example':
            create_fantasy_novel_example()
        elif args.mode == 'interactive':
            interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
