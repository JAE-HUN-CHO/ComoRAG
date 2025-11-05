# NovelForge 빠른 시작 가이드

## 📋 필수 요구사항

### 1. Python 환경
- Python 3.10 이상 필요
- pip 패키지 매니저

### 2. API 키
NovelForge를 사용하려면 LLM API 키가 필요합니다. 다음 중 하나를 선택하세요:

#### 옵션 A: OpenAI API (권장 - 가장 쉬움)
- **장점**: 설치 간단, 고품질 결과
- **단점**: 사용량에 따라 과금
- **가입**: https://platform.openai.com/signup
- **API 키 발급**: https://platform.openai.com/api-keys
- **가격**:
  - GPT-4o-mini: 매우 저렴 (소설 1장 생성에 약 $0.01~0.05)
  - GPT-4o: 고품질 (소설 1장 생성에 약 $0.10~0.50)

#### 옵션 B: 로컬 vLLM (무료, GPU 필요)
- **장점**: 무료, 데이터 프라이버시
- **단점**: GPU 필요, 설정 복잡
- **요구사항**: NVIDIA GPU (8GB+ VRAM 권장)

#### 옵션 C: 다른 OpenAI 호환 API
- **Claude API** (Anthropic)
- **Gemini API** (Google)
- **국내 서비스**: Upstage, Wrtn, 네이버 HyperCLOVA 등

---

## 🚀 설치 및 실행 (5분 완성)

### Step 1: 저장소 클론

```bash
git clone https://github.com/JAE-HUN-CHO/ComoRAG.git
cd ComoRAG
```

### Step 2: 의존성 설치

```bash
pip install -r requirements.txt
```

주요 패키지:
- `openai`: OpenAI API 클라이언트
- `igraph`: 캐릭터 관계 그래프
- `transformers`: 토크나이저
- `python-igraph`: 그래프 라이브러리

### Step 3: API 키 설정

#### 방법 1: 환경 변수 (권장)

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 선택사항
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

#### 방법 2: .env 파일 생성

프로젝트 루트에 `.env` 파일 생성:

```bash
# .env 파일
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

그리고 Python 코드에서:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### 방법 3: 코드에 직접 입력 (테스트용)

`main_novel_writer.py` 수정:
```python
config = NovelConfig(
    llm_api_key='sk-your-api-key-here',  # 직접 입력
    llm_base_url='https://api.openai.com/v1',
    llm_name='gpt-4o-mini',
    # ...
)
```

⚠️ **보안 주의**: 실제 키를 코드에 넣지 말고 환경 변수 사용 권장!

### Step 4: 실행!

#### 예제 실행 (판타지 소설 자동 생성)
```bash
python main_novel_writer.py --mode example
```

이렇게 하면:
1. 캐릭터 3명 생성 (주인공, 조력자, 악당)
2. 플롯 포인트 4개 추가
3. 오프닝 씬 2개 자동 생성
4. 일관성 검사
5. Markdown과 JSON으로 내보내기

출력 위치: `novels/The_Last_Sage/`

#### 대화형 모드 (직접 만들기)
```bash
python main_novel_writer.py --mode interactive
```

단계별로:
1. 소설 제목 입력
2. 장르 선택
3. 캐릭터 생성
4. 플롯 추가
5. 장면 생성

---

## 💰 비용 예상 (OpenAI 사용 시)

### GPT-4o-mini (권장)
- **가격**: 입력 $0.15/1M 토큰, 출력 $0.60/1M 토큰
- **예상 비용**:
  - 짧은 장면 (500단어): $0.01~0.03
  - 긴 장면 (2000단어): $0.05~0.10
  - 전체 챕터 (5000단어): $0.15~0.30
  - 중편 소설 (50,000단어): $1.50~3.00

### GPT-4o (고품질)
- **가격**: 입력 $2.50/1M 토큰, 출력 $10.00/1M 토큰
- **예상 비용**: 약 10배 비쌈
- **추천**: 최종 장면이나 중요한 부분만 사용

### 무료 대안
1. **로컬 모델** (vLLM + Llama 3 등)
2. **무료 API**: Groq (일일 한도 있음)

---

## 📝 빠른 테스트

### 최소한의 코드로 테스트:

```python
from src.comorag.NovelWriter import NovelWriter, NovelConfig
import os

# 설정
config = NovelConfig(
    llm_api_key=os.getenv('OPENAI_API_KEY'),
    llm_name='gpt-4o-mini',
    novel_title='테스트 소설',
    genre='fantasy',
    output_dir='novels'
)

# 초기화
novel = NovelWriter(config=config)

# 캐릭터 생성
novel.create_character(
    name="주인공",
    personality="용감하고 호기심 많음",
    background="평범한 학생이었으나 마법을 발견함"
)

# 장면 생성
scene = novel.generate_scene(
    chapter=1,
    scene_number=1,
    prompt="주인공이 처음으로 마법을 발견하는 순간",
    characters=["주인공"],
    tone="신비롭고 경이로운"
)

print(scene)

# 저장
novel.save_project()
```

이 코드를 `test_novel.py`로 저장하고 실행:
```bash
python test_novel.py
```

---

## ⚙️ 고급 설정

### 임베딩 모델 사용 (선택사항)

더 나은 컨텍스트 검색을 위해:

```python
config = NovelConfig(
    # LLM 설정
    llm_api_key='...',
    llm_name='gpt-4o-mini',

    # 임베딩 모델 추가
    embedding_model_name='sentence-transformers/all-MiniLM-L6-v2',
    embedding_batch_size=32,

    # ...
)
```

필요한 경우:
```bash
pip install sentence-transformers
```

### vLLM 로컬 모델 사용

```bash
# 1. vLLM 설치
pip install vllm

# 2. 모델 다운로드 (예: Llama 3)
# Hugging Face에서 자동 다운로드됨

# 3. vLLM 서버 시작
vllm serve meta-llama/Llama-3-8B-Instruct \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9

# 4. NovelForge 설정
config = NovelConfig(
    llm_base_url='http://localhost:8000/v1',
    llm_name='meta-llama/Llama-3-8B-Instruct',
    llm_api_key='dummy',  # 로컬이라 아무거나
    # ...
)
```

---

## 🐛 문제 해결

### 1. "ImportError: No module named..."
```bash
pip install -r requirements.txt
```

### 2. "OpenAI API key not found"
환경 변수 확인:
```bash
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows CMD
```

### 3. "Rate limit exceeded"
- 잠시 기다리거나
- API 플랜 업그레이드
- 토큰 제한 낮추기:
```python
config = NovelConfig(
    max_tokens_scene=1000,  # 기본 2000에서 줄임
    # ...
)
```

### 4. 생성 품질이 낮음
- GPT-4o로 변경
- 프롬프트 개선
- 더 자세한 캐릭터 프로필 작성

---

## 📚 다음 단계

1. ✅ 기본 실행 완료
2. 📖 [README.md](README.md) 읽기 - 전체 기능 이해
3. 📖 [README_ko.md](README_ko.md) 읽기 - 한국어 상세 가이드
4. 🎯 예제 템플릿 확인: `examples/fantasy_template.json`
5. 💻 API 문서 보기 (각 모듈의 docstring)

---

## 💡 팁

### 비용 절약
- `gpt-4o-mini` 사용 (품질도 좋고 저렴)
- `max_tokens` 조절
- 캐시 활용 (같은 캐릭터 반복 사용)

### 품질 향상
- 자세한 캐릭터 프로필 작성
- 명확한 장면 프롬프트
- 정기적인 일관성 체크

### 워크플로우
1. 먼저 전체 아웃라인 작성
2. 주요 캐릭터 모두 정의
3. 챕터별로 장면 생성
4. 5챕터마다 일관성 체크
5. 최종 검토 후 내보내기

---

## 🆘 도움이 필요하면

- 📧 Issue: https://github.com/JAE-HUN-CHO/ComoRAG/issues
- 📚 문서: README.md, README_ko.md
- 💬 코드 주석 참고

---

즐거운 소설 작성 되세요! 📖✨
