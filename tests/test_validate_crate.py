import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validate_ozx_ro_crate import validate  # noqa: E402


def load(crate_path: str):
    return json.loads(Path(crate_path).read_text(encoding="utf-8"))


def test_example_production_crate_has_no_errors():
    data = load("src/examples/valid/example_production_crate.json")
    errors, warnings = validate(data)
    assert errors == []
    assert isinstance(warnings, list)


def test_compliant_crate_has_no_errors():
    data = load("src/examples/valid/compliant_crate.json")
    errors, warnings = validate(data)
    assert errors == []
    assert isinstance(warnings, list)


def test_missing_root_reports_errors():
    data = load("src/examples/invalid/missing_root.json")
    errors, warnings = validate(data)
    assert errors  # must report missing root
    assert isinstance(warnings, list)


def test_missing_metadata_reports_errors():
    data = load("src/examples/invalid/missing_metadata.json")
    errors, warnings = validate(data)
    assert errors  # must report missing metadata descriptor
    assert isinstance(warnings, list)


def test_broken_chain_reports_errors():
    data = load("src/examples/invalid/broken_chain.json")
    errors, warnings = validate(data)
    assert errors  # must report missing specimen/biosample chain
    assert isinstance(warnings, list)
