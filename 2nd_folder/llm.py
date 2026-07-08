from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

from openai import OpenAI


DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OLLAMA_MODEL = "qwen2.5:7b"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_LM_STUDIO_URL = "http://localhost:1234/v1"


def _load_dotenv(dotenv_path: Path | None = None) -> None:
    if dotenv_path is None:
        dotenv_path = Path(".env")
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


_load_dotenv()


def ask_llm(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
    max_retries: int = 3,
) -> str:
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()

    if model is None:
        if provider == "openai":
            model = os.getenv("LLM_MODEL", DEFAULT_OPENAI_MODEL)
        elif provider == "groq":
            model = os.getenv("LLM_MODEL", DEFAULT_GROQ_MODEL)
        else:
            model = os.getenv("LLM_MODEL", DEFAULT_OLLAMA_MODEL)

    last_error = None
    for attempt in range(max_retries):
        try:
            if provider == "ollama":
                return _ask_ollama(system_prompt, user_prompt, model)
            if provider == "lmstudio":
                return _ask_openai_compatible(
                    system_prompt, user_prompt,
                    model=model,
                    base_url=os.getenv("LM_STUDIO_BASE_URL", DEFAULT_LM_STUDIO_URL),
                    api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
                )
            if provider == "openai":
                return _ask_openai_compatible(
                    system_prompt, user_prompt,
                    model=model,
                    base_url=None,
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
            if provider == "groq":
                return _ask_openai_compatible(
                    system_prompt, user_prompt,
                    model=model,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.getenv("GROQ_API_KEY"),
                )
            raise ValueError("LLM_PROVIDER must be one of: openai, ollama, lmstudio, groq")
        except Exception as exc:
            last_error = exc
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"LLM call failed: {exc}. Retrying in {wait}s...")
                time.sleep(wait)

    raise RuntimeError(f"LLM call failed after {max_retries} retries") from last_error


def _ask_openai_compatible(
    system_prompt: str,
    user_prompt: str,
    model: str,
    base_url: str | None,
    api_key: str | None,
) -> str:
    if not api_key:
        raise RuntimeError("API key is required for the selected LLM provider.")

    client = OpenAI(base_url=base_url, api_key=api_key) if base_url else OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def _ask_ollama(system_prompt: str, user_prompt: str, model: str) -> str:
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
