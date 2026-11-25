"""Archive of conversations with the agent.

Each session is saved in two files:
    *.jsonl — full data (one event per line), for programmatic use
    *.md    — human-readable version

Location: ~/.local/share/tooled-ai-agent/sessions/YYYY/MM/
(can be changed via the TOOLED_AI_AGENT_HOME environment variable).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir

QUESTION_MARK = "## ❯ "     # question marker in .md — we search based on this
MAX_MD_TOOL_RESULT = 300    # truncate long tool outputs in .md files

_TRANSLIT = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e", "є": "ie",
    "ж": "zh", "з": "z", "и": "y", "і": "i", "ї": "i", "й": "i", "к": "k", "л": "l",
    "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ь": "",
    "ю": "iu", "я": "ia", "ё": "e", "ы": "y", "э": "e", "ъ": "",
})

def sessions_dir() -> Path:
    base = os.getenv("TOOLED_AI_AGENT_HOME") or user_data_dir("tooled-ai-agent", appauthor=False)
    return Path(base) / "sessions"

def slugify(text: str, max_len: int = 40) -> str:
    """'Порахуй 15% від 2400' -> 'porakhui-15-vid-2400'."""
    text = text.lower().translate(_TRANSLIT)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len].rstrip("-") or "session"

class SessionLog:
    """Records a single conversation session in .jsonl and .md formats.

    Files are created only upon the first question—empty sessions do not clutter the archive.
    """

    def __init__(self, model_name: str, model_id: str) -> None:
        self.model_name = model_name
        self.model_id = model_id
        self.started = datetime.now()
        self.jsonl_path: Path | None = None
        self.md_path: Path | None = None

    #----------------------------------------------------
    # public methods
    #----------------------------------------------------

    def log_user(self, text: str) -> None:
        if self.jsonl_path is None:
            self._create_files(first_question=text)
        self._event("user", content=text)
        first, _, rest = text.strip().partition("\n")
        md = f"\n{QUESTION_MARK}{first}\n"
        if rest:
            md += f"\n{rest}\n"
        self._md(md)

    def log_tool(self, name: str, args: dict[str, Any], result: str) -> None:
        self._event("tool", name=name, args=args, result=result)
        short = " ".join(str(result).split())
        if len(short) > MAX_MD_TOOL_RESULT:
            short = short[: MAX_MD_TOOL_RESULT - 1] + "…"
        self._md(f"> 🔧 `{name}({json.dumps(args, ensure_ascii=False)})` → {short}\n")

    def log_answer(self, text: str, tokens_in: int = 0, tokens_out: int = 0) -> None:
        self._event("assistant", content=text, model=self.model_name,
                    tokens_in=tokens_in, tokens_out=tokens_out)
        self._md(f"\n{text.strip()}\n\n*↑ {tokens_in:,} ↓ {tokens_out:,} tokens · {self.model_name}*\n")

    def log_event(self, kind: str, text: str = "", **data: Any) -> None:
        """System events: model change, cancellation, error, history clearing."""
        if kind == "model":
            self.model_name = data.get("name", self.model_name)
            self.model_id = data.get("model", self.model_id)
        self._event(kind, text=text, **data)
        if text:
            self._md(f"\n> ⚠ {text}\n")

    #----------------------------------------------------
    # internal methods
    #----------------------------------------------------

    def _create_files(self, first_question: str) -> None:
        folder = sessions_dir() / self.started.strftime("%Y/%m")
        folder.mkdir(parents=True, exist_ok=True)
        stem = f"{self.started:%Y-%m-%d_%H%M%S}_{slugify(first_question)}"
        self.jsonl_path = folder / f"{stem}.jsonl"
        self.md_path = folder / f"{stem}.md"

        title = first_question.strip().split("\n")[0][:100]
        self._event("session", model=self.model_name, model_id=self.model_id)
        self._md(f"# {title}\n*{self.started:%Y-%m-%d %H:%M} · "
                 f"{self.model_name} ({self.model_id})*\n")

    def _event(self, kind: str, **data: Any) -> None:
        if self.jsonl_path is None:
            return  # no questions yet — we aren't writing anything
        record = {"ts": datetime.now().isoformat(timespec="seconds"), "type": kind, **data}
        with self.jsonl_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    def _md(self, text: str) -> None:
        if self.md_path is None:
            return
        with self.md_path.open("a", encoding="utf-8") as f:
            f.write(text)

#----------------------------------------------------
# search the archive
#----------------------------------------------------

@dataclass
class SessionInfo:
    path: Path
    title: str
    date: str

@dataclass
class SearchHit:
    path: Path
    line_no: int
    date: str
    question: str

def _md_files() -> list[Path]:
    """All .md files in the archive, from newest to oldest."""
    root = sessions_dir()
    if not root.exists():
        return []
    return sorted(root.rglob("*.md"), key=lambda p: p.name, reverse=True)

def _date_from_name(path: Path) -> str:
    # 2026-11-24_031305_slug.md -> 2026-11-24 03:13
    m = re.match(r"(\d{4}-\d{2}-\d{2})_(\d{2})(\d{2})", path.name)
    return f"{m[1]} {m[2]}:{m[3]}" if m else "?"

def list_sessions(limit: int = 10) -> list[SessionInfo]:
    result = []
    for path in _md_files()[:limit]:
        with path.open(encoding="utf-8") as f:
            first = f.readline().strip()
        result.append(SessionInfo(path, first.lstrip("# ") or path.stem, _date_from_name(path)))
    return result


def search(query: str, limit: int = 20) -> list[SearchHit]:
    """Searches for questions containing ALL query words (case-insensitive)."""
    words = query.lower().split()
    if not words:
        return []
    hits: list[SearchHit] = []
    for path in _md_files():
        with path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if line.startswith(QUESTION_MARK):
                    question = line[len(QUESTION_MARK):].strip()
                    if all(w in question.lower() for w in words):
                        hits.append(SearchHit(path, line_no, _date_from_name(path), question))
                        if len(hits) >= limit:
                            return hits
    return hits
