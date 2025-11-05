<h1 align="center">NovelForge: AI-Powered Long-Form Novel Writing Framework</h1>
<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/) [![CUDA](https://img.shields.io/badge/CUDA-12.x-green)](https://developer.nvidia.com/cuda-zone) [![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)](https://kernel.org/) [![LLM](https://img.shields.io/badge/LLM-OpenAI%2FvLLM-purple)](#main-modules) [![Status](https://img.shields.io/badge/Status-Active-success)](#) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[한국어](README_ko.md) | [English](README.md)

</div>

---

## Project Introduction
**NovelForge** is an AI-powered framework for writing long-form novels with consistency, coherence, and creative depth. Inspired by cognitive memory systems, it helps authors manage complex narratives by organizing characters, plotlines, world-building, and maintaining narrative consistency throughout the story.

✨ What makes NovelForge different?

Writing long novels is challenging due to intricate plotlines, evolving character arcs, and the need to maintain consistency across hundreds of pages. Traditional writing tools lack the intelligence to track narrative elements and ensure coherence.

NovelForge takes a **cognition-inspired approach**: novel writing is not linear, but a dynamic process of creating, organizing, and refining narrative elements — analogous to how writers think and plan. 🧠

- 📚 **Character Management**: Track characters, their relationships, development arcs, and ensure consistent personalities
- 🗺️ **Plot Structure**: Organize chapters, scenes, and plot points with timeline management
- 🌍 **World Building**: Maintain consistent settings, rules, and background lore
- 🔄 **Consistency Checking**: AI-powered validation of character actions, timeline, and plot coherence
- 🎯 **Scene Generation**: Generate scenes, dialogues, and descriptions while maintaining narrative flow
- 🧳 **Memory System**: Hierarchical memory (setting/theme/events) ensures long-term consistency

🚀 Key Features: NovelForge enables writers to focus on creativity while the AI handles consistency tracking, suggests plot developments, generates scenes, and maintains narrative coherence across long manuscripts. 📈

**Core workflow**: Plan → Create → Track → Validate → Refine → Generate. 🧩

---

## Key Features ✨
- 🧠 Support for various LLMs (OpenAI, vLLM) for intelligent content generation
- 👥 **Character System**: Create, track, and manage character profiles with relationship graphs
- 📖 **Plot Management**: Hierarchical chapter/scene structure with timeline tracking
- 🌍 **World Building**: Organize settings, lore, rules in structured knowledge base
- 🔄 **Consistency Engine**: AI validates character behavior, plot coherence, timeline accuracy
- 🎨 **Scene Generator**: Create scenes, dialogues, descriptions matching your style
- 🧱 **Memory Architecture**: Multi-layer memory (Setting/Theme/Event) for long-term consistency
- 📝 **Modular & Extensible**: Easy to customize and extend

---

## Directory Structure 📂
```
NovelForge/
├── main_novel_writer.py                 # Main novel writing interface
├── main_openai.py                       # Novel writing with OpenAI API
├── main_vllm.py                         # Novel writing with local vLLM
├── examples/                            # Example novels and templates
│   ├── fantasy_template.json            # Fantasy novel template
│   └── mystery_template.json            # Mystery novel template
├── src/novelforge/                      # Core code
│   ├── NovelWriter.py                   # Main novel writing class
│   ├── character_manager.py             # Character management system
│   ├── plot_manager.py                  # Plot structure and timeline
│   ├── scene_generator.py               # Scene generation engine
│   ├── consistency_checker.py           # Consistency validation
│   ├── world_builder.py                 # World building management
│   ├── utils/                           # Utility modules
│   ├── embedding_model/                 # Embedding models
│   ├── llm/                             # LLM integration
│   ├── prompts/                         # Novel writing prompts
│   └── memory_system.py                 # Hierarchical memory system
├── requirements.txt                     # Dependencies
└── README.md                            # Project documentation
```

---

## Installation & Environment 🛠️
1. 🐍 **Python version**: Python 3.10 or above recommended
2. 📦 **Install dependencies**:
```bash
pip install -r requirements.txt
```
3. 🔑 **Environment variables**: Set your OpenAI API Key or local LLM/embedding paths as needed
4. ⚙️ **GPU (optional but recommended)**: CUDA 12.x supported by many dependencies in requirements.txt

---

## Data Preparation & Format 📄

NovelForge uses JSON format for novel projects:

### Novel Project Structure
```json
{
  "title": "My Novel Title",
  "genre": "fantasy",
  "characters": [...],
  "plot": {...},
  "world": {...},
  "chapters": [...]
}
```

### Character Definition
```json
{
  "name": "Character Name",
  "age": 25,
  "personality": "brave, curious",
  "background": "...",
  "relationships": [{"with": "Other Character", "type": "friend"}]
}
```

---

## Quick Start ⚡

### Method 1: Interactive Novel Creation 🚀

```bash
python main_novel_writer.py --mode interactive
```

This launches an interactive session where you can:
- Create characters and define relationships
- Outline plot structure and major events
- Generate scenes chapter by chapter
- Validate consistency as you write

### Method 2: Using OpenAI API (main_openai.py) 🚀

1. Configure your novel project:
```python
config = NovelConfig(
    llm_base_url='https://api.openai.com/v1',
    llm_name='gpt-4o',
    novel_title='The Dragon Chronicles',
    genre='fantasy',
    embedding_model_name='/path/to/your/embedding/model',
    output_dir='novels/dragon_chronicles',
    max_tokens_scene=2000,  # Tokens per scene
    max_tokens_dialogue=1500,  # Tokens for dialogue
    consistency_check=True,  # Enable consistency validation
    style_guide='descriptive, vivid imagery'
)
```

2. Run the novel writer ▶️:
```bash
python main_openai.py
```

### Method 3: Using Local vLLM Server (main_vllm.py) ⚡

#### 1. Start vLLM Server 🚀

First, start the vLLM OpenAI-compatible API server:

```bash
# Method 1: Using vllm serve command
vllm serve /path/to/your/model \
  --tensor-parallel-size 1 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.95

# Method 2: Using python -m vllm.entrypoints.openai.api_server
python -m vllm.entrypoints.openai.api_server \
  --model /path/to/your/model \
  --served-model-name your-model-name \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --dtype auto
```

**Parameter descriptions:**
- `--model`: Model path (e.g., `/path/to/your/model`)
- `--tensor-parallel-size`: Number of GPU parallel processes
- `--max-model-len`: Maximum model length
- `--gpu-memory-utilization`: GPU memory utilization rate

#### 2. Configure main_vllm.py 📝

Modify the configuration in `main_vllm.py`:

```python
# vLLM server configuration
vllm_base_url = 'http://localhost:8000/v1'
served_model_name = '/path/to/your/model'

config = NovelConfig(
    llm_base_url=vllm_base_url,
    llm_name=served_model_name,
    llm_api_key="your-api-key-here",  # Any value for local server
    novel_title='My Fantasy Novel',
    genre='fantasy',
    embedding_model_name='/path/to/your/embedding/model',
    output_dir='novels/fantasy_novel',
    max_tokens_scene=2000,
    consistency_check=True
)
```

#### 3. Run the Program ▶️

```bash
python main_vllm.py
```

#### 4. Check Server Status 🔍

Ensure the vLLM server is running properly:

```bash
# Check if port is occupied
netstat -tlnp | grep 8000

# Test API connection
curl http://localhost:8000/v1/models
```

### Comparison of Methods 📊

| Feature | OpenAI API | vLLM Local | Interactive |
|---------|------------|------------|-------------|
| Cost | Pay per token | One-time download | Same as base method |
| Speed | Network latency | Local, faster | Interactive pace |
| Privacy | Cloud | Fully local | Same as base method |
| Setup | Simple | Needs GPU | Easiest |
| Control | API limits | Full control | Most flexible |

📁 Generated novels saved under `novels/<project_name>/`

---

## Main Modules 📦

### Core Components
- 📖 **`NovelWriter.py`**: Main novel generation orchestrator
- 👥 **`character_manager.py`**: Character creation, tracking, relationship graphs
- 🗺️ **`plot_manager.py`**: Chapter structure, timeline, plot points
- 🎨 **`scene_generator.py`**: AI-powered scene and dialogue generation
- 🔍 **`consistency_checker.py`**: Validates character behavior, timeline, plot logic
- 🌍 **`world_builder.py`**: Manages settings, lore, rules, world details

### Supporting Systems
- 🧰 **`utils/`**: Memory system, configuration, logging, agents
- 🧲 **`embedding_model/`**: Text embedding for semantic search
- 🤖 **`llm/`**: LLM integration (OpenAI, vLLM)
- 🗒️ **`prompts/`**: Novel-specific prompt templates (scene generation, character dialogue, etc.)
- 📦 **`memory_system.py`**: Hierarchical memory (Setting/Theme/Event) for consistency

---

## Usage Examples 🎯

### Creating a Fantasy Novel

```python
from src.novelforge import NovelWriter, CharacterManager, PlotManager

# Initialize novel project
novel = NovelWriter(
    title="The Last Mage",
    genre="fantasy",
    llm_name="gpt-4o"
)

# Create characters
char_mgr = novel.character_manager
protagonist = char_mgr.create_character(
    name="Aria",
    age=24,
    personality="brave, determined, curious",
    background="Last surviving mage in a world where magic is forbidden"
)

# Define plot structure
plot_mgr = novel.plot_manager
plot_mgr.add_plot_point(
    chapter=1,
    event="Aria discovers her magical abilities",
    importance="critical"
)

# Generate scenes
scene = novel.generate_scene(
    chapter=1,
    scene_number=1,
    prompt="Aria's ordinary day is interrupted by a magical incident",
    tone="mysterious, tense"
)

# Check consistency
novel.check_consistency()

# Export novel
novel.export(format="markdown", output_path="novels/the_last_mage.md")
```

### Interactive Mode

```bash
python main_novel_writer.py --mode interactive

# Follow prompts:
# 1. Enter novel title and genre
# 2. Create characters
# 3. Outline major plot points
# 4. Generate chapters scene by scene
# 5. Review and refine
```

---

## Contact & Contribution 🤝
For questions or suggestions, feel free to submit an Issue or PR.

---

## Acknowledgement 🙏
This framework is inspired by cognitive memory systems research and builds upon narrative AI techniques. Original RAG architecture adapted from [ComoRAG](https://arxiv.org/abs/2508.10419).
