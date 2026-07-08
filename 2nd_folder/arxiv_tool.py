import os
import time
from pathlib import Path

import arxiv
from arxiv import HTTPError
from pypdf import PdfReader


MAX_PAPER_CHARS = 30000


def search_arxiv(query: str, max_results: int = 5) -> list[arxiv.Result]:
    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=5.0,
        num_retries=5,
    )
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
    work_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = work_dir / f"{paper.get_short_id().replace('/', '_')}.pdf"

    print(f"Downloading PDF from: {paper.pdf_url}")
    paper.download_pdf(filename=str(pdf_path))

    text_parts = []
    reader = PdfReader(str(pdf_path))
    for page_index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        text_parts.append(f"\n--- Page {page_index} ---\n{page_text}")

    pdf_path.unlink(missing_ok=True)
    return "\n".join(text_parts)[:MAX_PAPER_CHARS]
