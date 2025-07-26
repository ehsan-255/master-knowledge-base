import glob
import json
from jsonschema import validate

with open("../tools/scribe/schemas/plugin_manifest.schema.json", "r", encoding="utf-8") as f:
    schema = json.load(f)

def test_all_manifests_are_v22():
    # If no manifests exist yet, this test still passes by iterating zero files.
    for mf in glob.glob("../tools/scribe/actions/**/manifest.json", recursive=True):
        with open(mf, "r", encoding="utf-8") as f:
            doc = json.load(f)
        validate(doc, schema)
        assert str(doc["manifest_version"]).startswith("2.2")