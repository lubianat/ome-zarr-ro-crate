import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validate_ome-zarr-ro-crate import validate


def load(crate_path: str):
    return json.loads(Path(crate_path).read_text(encoding="utf-8"))


def test_example_production_crate_has_no_errors():
    data = load("src/examples/valid/example_production_crate.json")
    errors, warnings = validate(data)
    assert errors == []
    assert isinstance(warnings, list)


def test_example_with_extra_context_has_no_errors():
    data = load("src/examples/valid/example_with_extra_context.json")
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


def test_missing_context_terms_reports_errors():
    data = load("src/examples/invalid/missing_context_terms.json")
    errors, warnings = validate(data)
    assert errors
    assert any("context missing required OME-Zarr term definitions" in e for e in errors)
    assert isinstance(warnings, list)


def test_additional_context_entries_are_allowed():
    data = load("src/examples/valid/example_production_crate.json")
    data["@context"].append("https://example.org/custom/context")
    data["@context"].append({"@vocab": "https://example.org/vocab#"})
    errors, warnings = validate(data)
    assert errors == []
    assert isinstance(warnings, list)


def test_missing_required_context_terms_reports_errors():
    data = load("src/examples/valid/example_production_crate.json")
    data["@context"] = [data["@context"][0]]  # drop term definitions
    errors, warnings = validate(data)
    assert errors
    assert any("term definitions" in e for e in errors)
    assert isinstance(warnings, list)
