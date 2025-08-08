import json
import os
import pathlib
import time
from typing import List, Dict, Any

def write_dlq(surface: str, event_id: str, errors: List[str], truncated_payload: Dict[str, Any]) -> None:
    root = os.environ.get("SCRIBE_REPORT_DIR", "tools/reports")
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(root) / "dlq.jsonl"
    rec = {
        "ts": int(time.time()),
        "surface": surface,
        "event_id": event_id,
        "errors": errors,
        "payload": truncated_payload
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, separators=(",", ":")) + "\n")