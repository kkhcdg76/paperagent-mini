# Modular Paper Reader Agent

This folder is the "second step" version of the mini project.

The same idea from `1st_folder/paper_reader_agent.py` is split into files:

- `llm.py`: LLM API wrapper (OpenAI, Ollama, LM Studio, Groq)
- `arxiv_tool.py`: arXiv search and PDF text extraction
- `agent.py`: agent classes (PaperReaderAgent, MethodExtractionAgent, PrototypePlannerAgent, PrototypeWriterAgent)
- `workflow.py`: 7-step orchestration logic
- `main.py`: command-line entry point

## Pipeline

1. arXiv 검색
2. PDF 다운로드 및 텍스트 추출
3. 논문별 한국어 요약 생성 → `paper_summaries.md`
4. 전체 문헌 리뷰 작성 → `final_literature_review.md`
5. 구현 가능한 방법/수식/알고리즘 추출 → `method_extraction.md`
6. 단계별 구현 계획 생성 → `implementation_plan.md`
7. mock data 기반 프로토타입 코드 및 실행 가이드 생성 → `prototype.py`, `prototype_readme.md`

## Environment (.env)

Create a `.env` file in `2nd_folder/`:

```ini
# OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key_here

# Ollama (local)
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b
OLLAMA_URL=http://localhost:11434/api/chat

# Groq
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here

# LM Studio (local)
LLM_PROVIDER=lmstudio
LLM_MODEL=qwen2.5-7b-instruct
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

## Run

```bash
pip install openai arxiv pypdf
python main.py "LLM agents for scientific discovery"
```

Outputs are written to `outputs/`.
