from __future__ import annotations

from pathlib import Path
from typing import Iterable


ALLOWED_CONTRACT_STATUSES = frozenset({"approved", "frozen"})


def contract_status(contract_path: str | Path) -> str:
    path = Path(contract_path)
    if not path.exists():
        return "missing"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def require_contract_ready(
    contract_path: str | Path,
    *,
    allow_unapproved: bool = False,
    context: str = "module2 formal run",
    allowed_statuses: Iterable[str] = ALLOWED_CONTRACT_STATUSES,
) -> str:
    status = contract_status(contract_path)
    allowed = set(str(item) for item in allowed_statuses)
    if status in allowed or bool(allow_unapproved):
        return status
    expected = " or ".join(sorted(allowed))
    raise ValueError(
        f"{context} requires contract status {expected}; got {status!r} for {Path(contract_path).as_posix()}"
    )
