"""
MCP Server for PaperAgent-Mini.

Exposes paper-agent tools (arXiv search, summarization, prototype generation)
to Claude Desktop via stdio transport.

Usage:
    python mcp_server.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from agent import (
    MethodExtractionAgent,
    PaperReaderAgent,
    PaperSummary,
    PrototypePlannerAgent,
    PrototypeWriterAgent,
)
from arxiv_tool import read_arxiv_pdf, search_arxiv

server = Server("paperagent-mini")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_arxiv",
            description="arXiv에서 주제 관련 논문을 검색합니다. 논문 제목, ID, 초록을 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "검색할 연구 주제 (영어 권장)"},
                    "max_results": {"type": "integer", "description": "최대 검색 결과 수", "default": 5},
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="read_paper",
            description="논문 PDF를 다운로드하고 전체 텍스트를 추출합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string", "description": "arXiv 논문 ID (예: 2501.04227)"},
                    "topic": {"type": "string", "description": "연구 주제 (컨텍스트용)"},
                },
                "required": ["paper_id", "topic"],
            },
        ),
        Tool(
            name="summarize_paper",
            description="논문을 한국어로 요약합니다. Problem, Key idea, Method, Experiments, Limitations, 의의를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제"},
                    "title": {"type": "string", "description": "논문 제목"},
                    "abstract": {"type": "string", "description": "논문 초록"},
                    "full_text": {"type": "string", "description": "논문 전체 텍스트 (앞부분 30000자)"},
                },
                "required": ["topic", "title", "abstract", "full_text"],
            },
        ),
        Tool(
            name="write_literature_review",
            description="여러 논문 요약을 종합하여 한국어 문헌 조사 서평을 작성합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제"},
                    "summaries_json": {
                        "type": "string",
                        "description": "JSON 문자열: [{paper_id, title, abstract, summary}, ...]",
                    },
                },
                "required": ["topic", "summaries_json"],
            },
        ),
        Tool(
            name="extract_methods",
            description="논문 요약에서 구현 가능한 알고리즘, 수식, 설계 구조를 추출합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제"},
                    "summaries_json": {
                        "type": "string",
                        "description": "JSON 문자열: [{paper_id, title, abstract, summary}, ...]",
                    },
                },
                "required": ["topic", "summaries_json"],
            },
        ),
        Tool(
            name="write_implementation_plan",
            description="추출된 방법론을 바탕으로 단계별 구현 계획서를 한국어로 작성합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제"},
                    "method_text": {"type": "string", "description": "추출된 방법론 텍스트"},
                },
                "required": ["topic", "method_text"],
            },
        ),
        Tool(
            name="generate_prototype",
            description="구현 계획서를 바탕으로 mock data 기반 prototype.py 코드를 생성합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제"},
                    "implementation_plan": {"type": "string", "description": "구현 계획서 텍스트"},
                },
                "required": ["topic", "implementation_plan"],
            },
        ),
        Tool(
            name="run_full_pipeline",
            description="주제 입력 한 번으로 검색→요약→리뷰→방법추출→계획→프로토타입까지 전체 파이프라인 실행. 시간이 5~10분 소요됩니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "연구 주제 (영어 권장)"},
                    "max_papers": {"type": "integer", "description": "분석할 논문 수", "default": 2},
                },
                "required": ["topic"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_arxiv":
        topic = arguments["topic"]
        max_results = arguments.get("max_results", 5)
        papers = search_arxiv(topic, max_results=max_results)
        result = json.dumps(
            [
                {
                    "paper_id": p.get_short_id(),
                    "title": p.title,
                    "abstract": p.summary,
                    "pdf_url": p.pdf_url,
                }
                for p in papers
            ],
            ensure_ascii=False,
            indent=2,
        )
        return [TextContent(type="text", text=f"검색 결과 ({len(papers)}건):\n{result}")]

    if name == "read_paper":
        import arxiv

        paper_id = arguments["paper_id"]
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        paper = next(client.results(search))
        full_text = read_arxiv_pdf(paper, Path("outputs"))
        preview = full_text[:500] + "..." if len(full_text) > 500 else full_text
        return [TextContent(
            type="text",
            text=json.dumps({
                "title": paper.title,
                "paper_id": paper.get_short_id(),
                "full_text": full_text,
                "preview": preview,
                "char_count": len(full_text),
            }, ensure_ascii=False),
        )]

    if name == "summarize_paper":
        import arxiv

        topic = arguments["topic"]
        title = arguments["title"]
        abstract = arguments["abstract"]
        full_text = arguments["full_text"]

        dummy = arxiv.Result.__new__(arxiv.Result)
        dummy.title = title
        dummy.summary = abstract

        def fake_get_short_id(self):
            return ""
        dummy.get_short_id = fake_get_short_id.__get__(dummy)

        agent = PaperReaderAgent(topic=topic)
        summary = agent.summarize_paper(dummy, full_text)
        return [TextContent(
            type="text",
            text=json.dumps({
                "paper_id": summary.paper_id,
                "title": summary.title,
                "summary": summary.summary,
            }, ensure_ascii=False),
        )]

    if name == "write_literature_review":
        topic = arguments["topic"]
        summaries_raw = json.loads(arguments["summaries_json"])
        summaries = [
            PaperSummary(
                paper_id=s.get("paper_id", ""),
                title=s.get("title", ""),
                abstract=s.get("abstract", ""),
                summary=s.get("summary", ""),
            )
            for s in summaries_raw
        ]
        agent = PaperReaderAgent(topic=topic)
        review = agent.write_literature_review(summaries)
        return [TextContent(type="text", text=review)]

    if name == "extract_methods":
        topic = arguments["topic"]
        summaries_raw = json.loads(arguments["summaries_json"])
        summaries = [
            PaperSummary(
                paper_id=s.get("paper_id", ""),
                title=s.get("title", ""),
                abstract=s.get("abstract", ""),
                summary=s.get("summary", ""),
            )
            for s in summaries_raw
        ]
        agent = MethodExtractionAgent(topic=topic)
        method_text = agent.run(summaries)
        return [TextContent(type="text", text=method_text)]

    if name == "write_implementation_plan":
        topic = arguments["topic"]
        method_text = arguments["method_text"]
        agent = PrototypePlannerAgent(topic=topic)
        plan = agent.run(method_text)
        return [TextContent(type="text", text=plan)]

    if name == "generate_prototype":
        topic = arguments["topic"]
        implementation_plan = arguments["implementation_plan"]
        agent = PrototypeWriterAgent(topic=topic)
        code, readme = agent.run(implementation_plan)
        result = f"""# prototype.py

```python
{code}
```

# prototype_readme.md

{readme}
"""
        return [TextContent(type="text", text=result)]

    if name == "run_full_pipeline":
        topic = arguments["topic"]
        max_papers = arguments.get("max_papers", 2)

        papers = search_arxiv(topic, max_results=max_papers)
        reader = PaperReaderAgent(topic=topic)

        summaries = []
        for paper in papers:
            full_text = read_arxiv_pdf(paper, Path("outputs"))
            summaries.append(reader.summarize_paper(paper, full_text))

        review = reader.write_literature_review(summaries)

        method_agent = MethodExtractionAgent(topic=topic)
        method_text = method_agent.run(summaries)

        planner = PrototypePlannerAgent(topic=topic)
        plan = planner.run(method_text)

        writer = PrototypeWriterAgent(topic=topic)
        code, readme = writer.run(plan)

        result = f"""# 📊 Literature Review

{review}

---

# 🔧 Extracted Methods

{method_text}

---

# 📋 Implementation Plan

{plan}

---

# 💻 prototype.py

```python
{code}
```

---

# 📖 실행 안내

{readme}
"""
        return [TextContent(type="text", text=result)]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
