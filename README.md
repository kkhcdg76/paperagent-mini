# paperagent-mini

논문을 요약하고 핵심 로직을 기반으로 미니 프로토타입 소스코드(`prototype.py`)를 자동 생성하는 에이전트 프로젝트입니다.


---

## 주요 작업 내용

1. **arXiv 직접 검색 적용**
   - 하드코딩되어 있던 fallback 논문 ID 리스트를 제거하고, 사용자가 입력한 검색어로 실시간 arXiv 검색을 수행하도록 변경했습니다.
   
2. **한국어 요약 및 분석**
   - 요약문(`paper_summaries.md`), 종합 서평(`final_literature_review.md`), 구현 모델 계획서(`implementation_plan.md`) 등의 마크다운 산출물이 한국어로 생성되도록 프롬프트를 패치했습니다.
   
3. **프로토타입 코드 및 실행 가이드 생성**
   - 논문의 핵심 메커니즘을 흉내 내어 로컬에서 바로 실행해볼 수 있는 프로토타입 소스코드(`outputs/prototype.py`)와 가이드(`outputs/prototype_readme.md`)를 자동으로 구현해 줍니다.
   - 불필요하고 무거운 머신러닝 라이브러리(torch, transformers 등) 임포트를 방지하여 numpy나 표준 라이브러리만으로도 데모를 바로 띄울 수 있도록 설계했습니다.

---

## 폴더 구조 및 역할

* **1st_folder (단일 파일 에이전트)**
  - 하나의 스크립트(`paper_reader_agent.py`)에서 논문 검색, PDF 변환, 한글 요약, 프로토타입 파이썬 코드 생성을 일괄 처리하는 핵심 코드 파일들이 들어 있습니다.
* **2nd_folder (모듈화 에이전트)**
  - 에이전트 기능을 역할별(`agent.py`, `llm.py`, `arxiv_tool.py` 등)로 컴포넌트화하여 모듈식 워크플로우로 쪼개놓은 버전입니다.

---

## 실행 방법


### 1. 의존성 패키지 설치
```bash
pip install openai arxiv pypdf
```

### 2. .env 파일 설정
`1st_folder` 내부에 `.env` 파일을 만들고 모델 API 정보를 기입합니다. (기본 설정은 Ollama 로컬 구동입니다.)

* **Ollama (로컬 구동 시)**
  ```env
  LLM_PROVIDER=ollama
  LLM_MODEL=qwen2.5:7b
  OLLAMA_URL=http://localhost:11434/api/chat
  ```
* **OpenAI API 사용 시 (추천)**
  ```env
  LLM_PROVIDER=openai
  LLM_MODEL=gpt-4o-mini
  OPENAI_API_KEY=your_openai_api_key_here
  ```


### 3. 스크립트 실행
```bash
cd 1st_folder
python paper_reader_agent.py "ReAct Synergizing Reasoning and Acting in Language Models"
```

실행이 완료되면 `outputs/` 폴더 내부에 요약본과 함께 `prototype.py`가 생성됩니다. 아래 명령어로 프로토타입 코드를 실행해볼 수 있습니다.
```bash
python outputs/prototype.py
```
