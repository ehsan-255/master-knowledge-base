import json
import os
from tools.scribe.core.dlq import write_dlq

def test_dlq_writes_jsonl(tmp_path, monkeypatch):
    monkeypatch.setenv("SCRIBE_REPORT_DIR", str(tmp_path))
    write_dlq("file_system", "e1", ["err"], {"path":"/x"})
    f = tmp_path / "dlq.jsonl"
    assert f.exists()
    rec = json.loads(f.read_text().splitlines()[0])
    assert rec["surface"] == "file_system"
    assert rec["event_id"] == "e1"