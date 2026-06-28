from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any


def to_json(instance: Any) -> str:
    if not is_dataclass(instance):
        raise TypeError("JSON serialization target must be a dataclass instance.")
    return json.dumps(asdict(instance), ensure_ascii=False, indent=2)
