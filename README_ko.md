# NovelForge: AI 기반 장편 소설 작성 프레임워크

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[한국어](README_ko.md) | [English](README.md)

</div>

---

## 프로젝트 소개

**NovelForge**는 AI를 활용하여 일관성 있고 깊이 있는 장편 소설을 작성할 수 있도록 돕는 프레임워크입니다. 인지 메모리 시스템에서 영감을 받아, 작가가 복잡한 서사를 관리하고 캐릭터, 플롯, 세계관을 체계적으로 구축할 수 있도록 지원합니다.

### 주요 특징 ✨

- 📚 **캐릭터 관리**: 캐릭터 프로필, 관계도, 성장 아크 추적
- 📖 **플롯 구조화**: 챕터/장면 계층 구조, 타임라인 관리
- 🌍 **세계관 구축**: 설정, 규칙, 배경 지식 체계적 관리
- 🔄 **일관성 검증**: AI 기반 캐릭터 행동, 타임라인, 플롯 일관성 검사
- 🎨 **장면 생성**: 장면, 대화, 묘사 자동 생성
- 🧠 **메모리 시스템**: 계층적 메모리로 장기 일관성 유지
- 🤖 **LLM 통합**: OpenAI, vLLM 등 다양한 모델 지원

---

## 빠른 시작 ⚡

### 설치

```bash
# 저장소 클론
git clone https://github.com/yourusername/NovelForge.git
cd NovelForge

# 의존성 설치
pip install -r requirements.txt

# API 키 설정
export OPENAI_API_KEY="your-api-key"
```

### 기본 사용법

#### 1. 예제 실행

```bash
python main_novel_writer.py --mode example
```

판타지 소설 예제를 생성합니다.

#### 2. 대화형 모드

```bash
python main_novel_writer.py --mode interactive
```

단계별로 소설을 만들 수 있습니다:
1. 소설 제목과 장르 입력
2. 캐릭터 생성
3. 플롯 포인트 추가
4. 장면 생성
5. 일관성 검사 및 내보내기

---

## Python API 사용 예제

```python
from src.comorag.NovelWriter import NovelWriter, NovelConfig

# 설정
config = NovelConfig(
    llm_name='gpt-4o',
    novel_title='나의 판타지 소설',
    genre='fantasy',
    style_guide='서정적이고 몰입감 있는 문체'
)

# 소설 작가 초기화
novel = NovelWriter(config=config)

# 캐릭터 생성
protagonist = novel.create_character(
    name="이아리아",
    age=25,
    personality="용감하고 호기심 많으며 연민이 깊음",
    background="마지막 남은 마법사 가문의 후예"
)

# 플롯 포인트 추가
novel.add_plot_point(
    chapter=1,
    event="아리아가 금지된 마법서를 발견한다",
    importance="critical"
)

# 장면 생성
scene = novel.generate_scene(
    chapter=1,
    scene_number=1,
    prompt="아리아는 깊은 밤 폐허가 된 탑에서 고대 마법서를 발견한다",
    characters=["이아리아"],
    tone="신비롭고 긴장감 있는"
)

print(scene)

# 일관성 검사
report = novel.check_consistency()

# 소설 내보내기
novel.export(format="markdown")
```

---

## 디렉토리 구조 📂

```
NovelForge/
├── main_novel_writer.py          # 메인 실행 파일
├── src/comorag/
│   ├── NovelWriter.py            # 핵심 소설 작가 클래스
│   ├── character_manager.py      # 캐릭터 관리
│   ├── plot_manager.py           # 플롯 구조 관리
│   ├── scene_generator.py        # 장면 생성 엔진
│   ├── consistency_checker.py    # 일관성 검증
│   ├── world_builder.py          # 세계관 관리
│   └── prompts/templates/        # 프롬프트 템플릿
├── novels/                       # 생성된 소설 저장
└── examples/                     # 예제 템플릿
```

---

## 핵심 기능 상세

### 캐릭터 관리

```python
# 캐릭터 생성
char = novel.create_character(
    name="홍길동",
    personality="의협심이 강하고 재치있음",
    background="조선시대 의적"
)

# 관계 추가
novel.character_manager.add_relationship(
    "홍길동", "춘향", "romance", "서로 사랑하는 사이"
)

# 캐릭터 발전 추적
novel.character_manager.track_character_development(
    "홍길동",
    "의협심과 개인적 욕망 사이에서 갈등",
    chapter=5
)
```

### 플롯 관리

```python
# 챕터 생성
novel.plot_manager.create_chapter(
    number=1,
    title="운명의 시작",
    summary="주인공이 자신의 운명을 깨닫는 순간"
)

# 플롯 포인트 추가
novel.add_plot_point(
    chapter=1,
    event="마을이 공격받다",
    importance="critical",
    characters_involved=["홍길동"],
    consequences=["마을 사람들이 대피", "주인공의 각성"]
)

# 타임라인 분석
timeline = novel.plot_manager.get_timeline()
```

### 장면 생성

```python
# 장면 생성
scene = novel.generate_scene(
    chapter=1,
    scene_number=1,
    prompt="홍길동이 처음으로 초능력을 발현하는 순간",
    tone="극적이고 감동적인"
)

# 대화 생성
dialogue = novel.scene_generator.generate_dialogue(
    character1=char1,
    character2=char2,
    context="두 사람이 오랜만에 재회하다",
    topic="과거의 일들",
    emotion="씁쓸하지만 따뜻한"
)

# 묘사 생성
description = novel.scene_generator.generate_description(
    subject="고대 사원",
    description_type="setting",
    sensory_focus=["visual", "auditory"],
    mood="신비롭고 경외감을 주는"
)
```

### 일관성 검사

```python
# 전체 일관성 검사
report = novel.check_consistency()

print(f"발견된 문제: {report['total_issues']}개")
for issue in report['issues']:
    print(f"- [{issue['type']}] {issue['message']}")

# 개별 장면 검증
validation = novel.consistency_checker.validate_scene(
    scene_text=scene,
    characters=["홍길동"],
    context={}
)
```

---

## 고급 기능

### 스타일 맞춤 설정

```python
config = NovelConfig(
    style_guide="""
    - 문체: 간결하고 직설적
    - 시점: 1인칭 관찰자
    - 톤: 냉소적이지만 따뜻한
    - 특징: 내적 독백 활용
    """
)
```

### 임베딩 기반 컨텍스트 검색

```python
config = NovelConfig(
    embedding_model_name='/path/to/embedding/model',
    embedding_batch_size=32
)

# 유사 장면 자동 참조
# 이전 장면들 중 현재와 관련있는 것을 자동으로 찾아 컨텍스트로 제공
```

### 플롯 제안

```python
# AI가 다음 플롯 전개를 제안
suggestion = novel.plot_manager.suggest_next_plot_point(
    current_chapter=5
)
print(f"제안: {suggestion}")
```

---

## 내보내기 형식

### Markdown

```bash
novel.export(format="markdown")
```

```markdown
# 소설 제목

## Chapter 1

장면 내용...

---
```

### JSON

```bash
novel.export(format="json")
```

완전한 구조 데이터 (캐릭터, 플롯, 장면 등 모두 포함)

### 텍스트

```bash
novel.export(format="txt")
```

순수 텍스트 형식

---

## 설정 옵션

```python
NovelConfig(
    llm_name='gpt-4o',              # LLM 모델
    llm_base_url='...',             # API 엔드포인트
    novel_title='제목',              # 소설 제목
    genre='fantasy',                # 장르
    style_guide='문체 가이드',       # 스타일 지침
    max_tokens_scene=2000,          # 장면당 최대 토큰
    max_tokens_dialogue=1500,       # 대화당 최대 토큰
    consistency_check=True,         # 일관성 검사 활성화
    auto_save=True,                 # 자동 저장
    output_dir='novels',            # 출력 디렉토리
)
```

---

## 팁과 모범 사례

### 1. 프로젝트 구조화

먼저 전체 구조를 계획하세요:
- 주요 캐릭터 정의
- 핵심 플롯 포인트 설정
- 세계관 규칙 정리

### 2. 점진적 생성

한 번에 많은 장면을 생성하지 말고, 단계별로 생성하고 검토하세요.

### 3. 일관성 유지

정기적으로 일관성 검사를 실행하세요:

```python
# 매 5챕터마다 검사
if chapter % 5 == 0:
    novel.check_consistency()
```

### 4. 캐릭터 발전 추적

중요한 캐릭터 변화를 기록하세요:

```python
novel.character_manager.track_character_development(
    "주인공", "결정적 선택을 통해 성장", chapter=10
)
```

---

## 문제 해결

### LLM API 오류

```python
# 재시도 로직 추가
try:
    scene = novel.generate_scene(...)
except Exception as e:
    logger.error(f"생성 실패: {e}")
    # 재시도 또는 대체 방법
```

### 메모리 부족

긴 컨텍스트는 요약하여 사용:

```python
config = NovelConfig(
    max_tokens_scene=1500,  # 토큰 제한 낮추기
)
```

---

## 라이선스

MIT License

---

## 기여

이슈나 PR을 환영합니다!

---

## 감사의 글

이 프레임워크는 인지 메모리 시스템 연구와 서사 AI 기술에서 영감을 받았습니다.
