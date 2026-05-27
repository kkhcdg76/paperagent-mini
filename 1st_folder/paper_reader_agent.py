"""
Paper2Prototype Agent.

Goal:
1. Search arXiv for papers related to a topic (no fallbacks).
2. Download/read selected paper text.
3. Ask an LLM to summarize each paper in Korean.
4. Write a final literature review in Korean.
5. Extract implementable methods/formulas/algorithms in Korean.
6. Write a step-by-step implementation plan in Korean.
7. Generate prototype Python code (prototype.py) and a Korean README.

Run:
    python paper_reader_agent.py "LLM agents for scientific discovery"
"""

from __future__ import annotations

import os
import sys
import json
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import arxiv
from arxiv import HTTPError
from openai import OpenAI
from pypdf import PdfReader


OPENAI_MODEL_NAME = "gpt-4o-mini"
LOCAL_MODEL_NAME = "qwen2.5:7b"
MAX_PAPER_CHARS = 30000
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_LM_STUDIO_URL = "http://localhost:1234/v1"


def load_dotenv(dotenv_path: Path = Path(".env")) -> None:
    """Load KEY=VALUE pairs from a local .env file without extra packages."""
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass
class PaperSummary:
    paper_id: str
    title: str
    abstract: str
    summary: str


def ask_llm(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """Small LLM wrapper supporting OpenAI, Ollama, LM Studio, and Groq."""
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    if model is None:
        if provider == "openai":
            model = OPENAI_MODEL_NAME
        elif provider == "groq":
            model = "llama-3.3-70b-versatile"
        else:
            model = LOCAL_MODEL_NAME
    model = os.getenv("LLM_MODEL", model).strip()

    if provider == "ollama":
        return ask_ollama(system_prompt, user_prompt, model)
    if provider == "lmstudio":
        return ask_openai_compatible(
            system_prompt,
            user_prompt,
            model=model,
            base_url=os.getenv("LM_STUDIO_BASE_URL", DEFAULT_LM_STUDIO_URL),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
        )
    if provider == "openai":
        return ask_openai_compatible(
            system_prompt,
            user_prompt,
            model=model,
            base_url=None,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    if provider == "groq":
        return ask_openai_compatible(
            system_prompt,
            user_prompt,
            model=model,
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )

    raise ValueError("LLM_PROVIDER must be one of: openai, ollama, lmstudio, groq")


def ask_openai_compatible(
    system_prompt: str,
    user_prompt: str,
    model: str,
    base_url: str | None,
    api_key: str | None,
) -> str:
    """Call OpenAI or an OpenAI-compatible local/remote server such as LM Studio or Groq."""
    if not api_key:
        raise RuntimeError("API key is required for the selected LLM provider.")

    if base_url:
        client = OpenAI(base_url=base_url, api_key=api_key)
    else:
        client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""



def ask_ollama(system_prompt: str, user_prompt: str, model: str) -> str:
    """Call a local Ollama model, for example qwen2.5:7b or llama3.1:8b."""
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "options": {"temperature": 0.2},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL),
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Start it with `ollama serve` "
            "and make sure your model is pulled."
        ) from exc

    return result.get("message", {}).get("content", "")


def search_arxiv(query: str, max_results: int = 5) -> list[arxiv.Result]:
    """Search arXiv directly without fallbacks."""
    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=5.0,
        num_retries=5,
    )
    # Search title and abstract using query directly
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    for attempt in range(5):
        try:
            results = list(client.results(search))
            if results:
                return results
            print(f"No results found for query: {query}. Retrying...")
            time.sleep(2)
        except HTTPError as exc:
            if "429" not in str(exc) or attempt == 4:
                raise RuntimeError(f"arXiv search API failed with rate-limit or HTTP error: {exc}")
            wait_seconds = int(os.getenv("ARXIV_RETRY_WAIT_SECONDS", "5")) * (attempt + 1)
            print(f"arXiv is rate-limiting us. Waiting {wait_seconds}s and retrying...")
            time.sleep(wait_seconds)

    raise RuntimeError(f"Failed to find any papers on arXiv for: {query}")


def read_arxiv_pdf(paper: arxiv.Result, work_dir: Path) -> str:
    """Download a PDF, extract text, then remove the temporary file."""
    work_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = work_dir / f"{paper.get_short_id().replace('/', '_')}.pdf"
    
    print(f"Downloading PDF from: {paper.pdf_url}")
    request = urllib.request.Request(
        paper.pdf_url,
        headers={"User-Agent": "PaperReviewAgent/0.1 contact: local-study-project"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        pdf_path.write_bytes(response.read())

    text_parts = []
    reader = PdfReader(str(pdf_path))
    for page_index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        text_parts.append(f"\n--- Page {page_index} ---\n{page_text}")

    pdf_path.unlink(missing_ok=True)
    return "\n".join(text_parts)[:MAX_PAPER_CHARS]



def summarize_paper(topic: str, paper: arxiv.Result, full_text: str) -> PaperSummary:
    """Ask the LLM to produce a structured Korean summary for one paper."""
    system_prompt = (
        "You are a careful research assistant. "
        "Read papers for a beginner research group and explain them clearly in Korean."
    )
    user_prompt = f"""
Research topic:
{topic}

Paper title:
{paper.title}

Paper abstract:
{paper.summary}

Paper text:
{full_text}

아래 항목들을 포함하여 한국어로 명확하고 간결한 요약본을 작성해 주세요:
- Problem (논문이 해결하고자 하는 문제)
- Key idea (핵심 아이디어)
- Method (방법론 및 모델 구조)
- Experiments or evidence (실험 방식 및 결과 증거)
- Limitations (연구 한계점)
- Why this matters for our project (우리 프로젝트에 적용할 수 있는 의의)
"""
    summary = ask_llm(system_prompt, user_prompt)
    return PaperSummary(
        paper_id=paper.get_short_id(),
        title=paper.title,
        abstract=paper.summary,
        summary=summary,
    )


def write_paper_summaries(summaries: list[PaperSummary], output_dir: Path) -> None:
    """Save structured summaries for each paper to a markdown file in Korean."""
    lines = ["# 논문 요약 모음집 (Paper Summaries)\n"]
    for i, s in enumerate(summaries, start=1):
        lines.append(f"## {i}. {s.title}")
        lines.append(f"- **arXiv ID**: [{s.paper_id}](https://arxiv.org/abs/{s.paper_id})")
        lines.append(f"\n### 요약 내용\n{s.summary}\n")
        lines.append("---\n")
    
    out_path = output_dir / "paper_summaries.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved summaries to {out_path}")


def write_literature_review(topic: str, summaries: list[PaperSummary]) -> str:
    """Synthesize all paper summaries into one review in Korean."""
    joined = "\n\n".join(
        f"## {item.title}\nID: {item.paper_id}\n\n{item.summary}"
        for item in summaries
    )
    system_prompt = (
        "You are a research mentor. "
        "Synthesize papers into a literature review for a student team in Korean."
    )
    user_prompt = f"""
Research topic:
{topic}

Paper summaries:
{joined}

위 요약본들을 종합하여 한국어로 작성된 문헌 조사 서평(Literature Review)을 작성해 주세요.
반드시 아래 항목을 포함해야 합니다:
1. Overall research trend (전체적인 연구 동향)
2. Paper comparison table (논문 비교 표 - 마크다운 테이블 형식)
3. Common methods (공통적으로 많이 사용된 방법론)
4. Open problems (미해결 과제 및 한계점)
5. Project ideas our team could build next (우리 팀이 후속으로 개발/구현할 수 있는 프로젝트 아이디어)
"""
    return ask_llm(system_prompt, user_prompt)


def extract_implementable_method(topic: str, summaries: list[PaperSummary]) -> str:
    """Extract implementable core methods, formulas, or algorithms in Korean."""
    joined = "\n\n".join(
        f"Title: {item.title}\nSummary: {item.summary}"
        for item in summaries
    )
    system_prompt = (
        "You are an expert ML/SW implementation engineer. "
        "Extract concrete mathematical formulations, pseudo-codes, and core algorithms in Korean."
    )
    user_prompt = f"""
Research topic:
{topic}

Paper summaries:
{joined}

위 논문 요약들 중에서 **실제 코드로 구현할 수 있는 구체적인 알고리즘, 수학 공식, 또는 설계 구조**를 추출해 주세요.
작성 언어는 한국어로 작성하고, 마크다운 코드 블록이나 수식을 활용하여 엔지니어가 보고 구현 계획을 세울 수 있도록 자세히 설명해 주세요.
"""
    return ask_llm(system_prompt, user_prompt)


def write_implementation_plan(topic: str, method_text: str) -> str:
    """Generate a step-by-step development/implementation plan in Korean."""
    system_prompt = (
        "You are a technical project manager. "
        "Create a detailed, step-by-step implementation plan for a software developer in Korean."
    )
    user_prompt = f"""
Research topic:
{topic}

Extracted method:
{method_text}

이 추출된 방법론을 바탕으로, 실제 작동하는 미니 프로토타입 Python 코드(prototype.py)를 구현하기 위한 **단계별 개발 계획서**를 작성해 주세요.
한국어로 작성해야 하며, 아래 항목들을 구체적으로 채워주세요:
1. Requirements & dependencies (필요 환경 및 패키지)
2. Core modules (구현해야 할 핵심 함수/클래스 정의 및 설계)
3. Input/Output specifications (입출력 데이터 규격)
4. Step-by-step execution steps (구현할 기능 순서 및 검증 시나리오)
"""
    return ask_llm(system_prompt, user_prompt)


def generate_prototype_code(topic: str, implementation_plan: str) -> str:
    """Generate self-contained prototype Python code based on the plan."""
    system_prompt = (
        "You are an elite Python developer. Write clean, self-contained, working python code with mock data. "
        "Provide ONLY valid executable Python code in code blocks. Do not write markdown text outside the code block."
    )
    user_prompt = f"""
Research topic:
{topic}

Implementation Plan:
{implementation_plan}

위 개발 계획서에 명시된 핵심 아이디어를 동작하는 Python 코드로 구현해 주세요.
조건:
1. 외부 데이터가 없어도 테스트해볼 수 있도록 소스코드 내부에서 **가짜 데이터(Mock data)**를 자동 생성하여 작동 검증을 마쳐야 합니다.
2. 예외 처리와 직관적인 주석을 포함해 주세요 (주석은 한글로 작성).
3. markdown 코드 블록 형태로 Python 코드만 출력해 주세요.
4. **중요: transformers, torch, tensorflow, pytorch 등 설치 시간이 오래 걸리거나 환경 구성이 복잡한 외부 AI/딥러닝 패키지 수입(import)을 전면 금지합니다.** 
   - 딥러닝 모델의 복잡한 추론 과정은 단순한 파이썬 연산 및 규칙 기반 함수(혹은 random 모듈을 사용한 시뮬레이션)로 흉내 내어(Mocking/Simulation), 표준 라이브러리(json, math, random, urllib 등)나 numpy 정도만 설치되어 있다면 즉시 즉시 작동될 수 있도록 작성해 주세요.
5. **필수: 생성되는 Python 코드 파일의 맨 마지막에는 `if __name__ == '__main__':` 블록을 반드시 포함하여, 위에서 정의한 클래스/함수들이 가짜 데이터로 실제로 구동되고 `print()` 함수를 통해 터미널에 보기 좋게 실행 결과가 출력되는 메인 실행 코드가 작성되도록 하십시오.**
"""

    raw_code = ask_llm(system_prompt, user_prompt)
    
    # Strip markdown code blocks if any
    if "```python" in raw_code:
        raw_code = raw_code.split("```python", 1)[1].split("```", 1)[0]
    elif "```" in raw_code:
        raw_code = raw_code.split("```", 1)[1].split("```", 1)[0]
        
    return raw_code.strip()



def write_prototype_readme(topic: str, implementation_plan: str) -> str:
    """Create instructions on how to run the prototype in Korean."""
    system_prompt = (
        "You are a developer relations advocate. Write a clean README.md guide in Korean."
    )
    user_prompt = f"""
Research topic:
{topic}

Implementation Plan:
{implementation_plan}

위 계획에 따라 생성된 `prototype.py`를 어떻게 실행하고 검증해야 하는지 알려주는 **실행 안내 가이드(README.md)**를 한국어로 작성해 주세요.
포함할 항목:
1. 프로토타입 소개 (어떤 논문 아이디어를 어떻게 간단히 시뮬레이션하는지)
2. 설치 패키지 및 실행 커맨드
3. 실행 시 예상되는 터미널 출력 결과물 설명
"""
    return ask_llm(system_prompt, user_prompt)


def main() -> None:
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Please put OPENAI_API_KEY=your-key in .env before running.")

    topic = " ".join(sys.argv[1:]).strip()
    if not topic:
        topic = input("Research topic: ").strip()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # 1. Searching papers
    print(f"[1/7] Searching arXiv for: {topic}")
    papers = search_arxiv(topic, max_results=3)  # Use 3 papers for quick execution

    # 2. Reading papers
    summaries = []
    for index, paper in enumerate(papers, start=1):
        print(f"[2/7] Reading paper {index}/{len(papers)}: {paper.title}")
        full_text = read_arxiv_pdf(paper, output_dir)

        # 3. Summarizing papers
        print(f"[3/7] Summarizing paper {index}/{len(papers)}")
        summaries.append(summarize_paper(topic, paper, full_text))

    # Save structured summaries
    write_paper_summaries(summaries, output_dir)

    # 4. Writing literature review
    print("[4/7] Writing final literature review...")
    review = write_literature_review(topic, summaries)
    out_review_path = output_dir / "final_literature_review.md"
    out_review_path.write_text(review, encoding="utf-8")
    print(f"Saved review to {out_review_path}")

    # 5. Extracting implementable method
    print("[5/7] Extracting implementable methods...")
    method_text = extract_implementable_method(topic, summaries)
    out_method_path = output_dir / "method_extraction.md"
    out_method_path.write_text(method_text, encoding="utf-8")
    print(f"Saved method extraction to {out_method_path}")

    # 6. Writing implementation plan
    print("[6/7] Writing implementation plan...")
    plan_text = write_implementation_plan(topic, method_text)
    out_plan_path = output_dir / "implementation_plan.md"
    out_plan_path.write_text(plan_text, encoding="utf-8")
    print(f"Saved plan to {out_plan_path}")

    # 7. Generating prototype code
    print("[7/7] Generating prototype code...")
    code_text = generate_prototype_code(topic, plan_text)
    out_code_path = output_dir / "prototype.py"
    out_code_path.write_text(code_text, encoding="utf-8")
    print(f"Saved prototype to {out_code_path}")

    readme_text = write_prototype_readme(topic, plan_text)
    out_readme_path = output_dir / "prototype_readme.md"
    out_readme_path.write_text(readme_text, encoding="utf-8")
    print(f"Saved prototype README to {out_readme_path}")

    print("\nAll 7 steps completed successfully!")
    print(f"Check your outputs in: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
