import argparse, json
from pathlib import Path


def summarize(crate):
    graph = crate.get("@graph", [])
    datasets = [e for e in graph if e.get("@type") == "Dataset"]
    files = [e for e in graph if e.get("@type") == "File"]
    print("Datasets:")
    for d in datasets:
        print(f" - {d.get('@id')}: {d.get('name','')}")
        if "license" in d:
            print(f"   license: {d['license']}")
        if "hasPart" in d:
            parts = [p.get("@id") for p in d.get("hasPart", []) if isinstance(p, dict)]
            if parts:
                print(f"   hasPart: {', '.join(parts)}")
        if "additionalProperty" in d:
            props = [p.get("@id", p) for p in d.get("additionalProperty", []) if isinstance(p, dict)]
            if props:
                print(f"   additionalProperty: {', '.join(props)}")
    if not datasets:
        print(" - none found")

    print("\nFiles:")
    for f in files:
        print(f" - {f.get('@id')}: {f.get('encodingFormat','')}")
    if not files:
        print(" - none found")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Show a quick summary of crate datasets/files.")
    ap.add_argument("crate", nargs="?", default="examples/valid/example_production_crate.json")
    args = ap.parse_args()
    data = json.loads(Path(args.crate).read_text(encoding="utf-8"))
    summarize(data)
