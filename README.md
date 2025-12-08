A simple RO-Crate 1.2 profile specifying the practice at https://ome.github.io/ome2024-ngff-challenge/

Examples:
- Valid: `examples/valid/example_production_crate.json`, `examples/valid/compliant_crate.json`
- Invalid (for quick checks): `examples/invalid/missing_root.json`, `examples/invalid/missing_metadata.json`, `examples/invalid/broken_chain.json`

Validation helpers:
- Run the lean checker: `python3 validate_ozx_ro_crate.py examples/valid/example_production_crate.json`
- Tests (basic MUST-level checks on examples): `pytest -q`
