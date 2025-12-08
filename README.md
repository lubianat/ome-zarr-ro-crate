A simple RO-Crate 1.2 profile specifying the practice at https://ome.github.io/ome2024-ngff-challenge/

Examples:
- Valid: `examples/valid/example_production_crate.json`, `examples/valid/example_1.2_crate.json`, `examples/valid/example_with_extra_context.json`
- Invalid (for quick checks): `examples/invalid/missing_root.json`, `examples/invalid/missing_metadata.json`, `examples/invalid/broken_chain.json`, `examples/invalid/missing_context_terms.json`

Validation helpers:
- Run the lean checker: `python3 validate_ozx_ro_crate.py examples/valid/example_production_crate.json`
- Tests (basic MUST-level checks on examples): `pytest -q`
