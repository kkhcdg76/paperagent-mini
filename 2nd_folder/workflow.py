from pathlib import Path

from agent import (
    MethodExtractionAgent,
    PaperReaderAgent,
    PrototypePlannerAgent,
    PrototypeWriterAgent,
)
from arxiv_tool import read_arxiv_pdf, search_arxiv


def run_paper_reader(
    topic: str,
    max_papers: int = 3,
    output_dir: str = "outputs",
) -> list[Path]:
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    reader_agent = PaperReaderAgent(topic=topic)

    print(f"[1/7] Searching arXiv for: {topic}")
    papers = search_arxiv(topic, max_results=max_papers)

    summaries = []
    for index, paper in enumerate(papers, start=1):
        print(f"[2/7] Reading paper {index}/{len(papers)}: {paper.title}")
        full_text = read_arxiv_pdf(paper, out_dir)

        print(f"[3/7] Summarizing paper {index}/{len(papers)}")
        summaries.append(reader_agent.summarize_paper(paper, full_text))

    summaries_path = Path(reader_agent.write_paper_summaries(summaries, output_dir))
    print(f"Saved summaries to {summaries_path}")

    print("[4/7] Writing final literature review...")
    review = reader_agent.write_literature_review(summaries)
    review_path = out_dir / "final_literature_review.md"
    review_path.write_text(review, encoding="utf-8")
    print(f"Saved review to {review_path}")

    print("[5/7] Extracting implementable methods...")
    method_agent = MethodExtractionAgent(topic=topic)
    method_text = method_agent.run(summaries)
    method_path = out_dir / "method_extraction.md"
    method_path.write_text(method_text, encoding="utf-8")
    print(f"Saved method extraction to {method_path}")

    print("[6/7] Writing implementation plan...")
    planner_agent = PrototypePlannerAgent(topic=topic)
    plan_text = planner_agent.run(method_text)
    plan_path = out_dir / "implementation_plan.md"
    plan_path.write_text(plan_text, encoding="utf-8")
    print(f"Saved plan to {plan_path}")

    print("[7/7] Generating prototype code...")
    writer_agent = PrototypeWriterAgent(topic=topic)
    code_text, readme_text = writer_agent.run(plan_text)

    code_path = out_dir / "prototype.py"
    code_path.write_text(code_text, encoding="utf-8")
    print(f"Saved prototype to {code_path}")

    readme_path = out_dir / "prototype_readme.md"
    readme_path.write_text(readme_text, encoding="utf-8")
    print(f"Saved prototype README to {readme_path}")

    print("\nAll 7 steps completed successfully!")
    print(f"Check your outputs in: {out_dir.resolve()}")

    return [
        summaries_path,
        review_path,
        method_path,
        plan_path,
        code_path,
        readme_path,
    ]
