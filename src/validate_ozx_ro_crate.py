import argparse, json
from pathlib import Path


def validate(crate):
    errors, warnings = [], []
    graph = crate.get("@graph", [])
    idx = {e.get("@id"): e for e in graph if isinstance(e, dict) and "@id" in e}

    # basic context check
    ctx = crate.get("@context")
    allowed = {
        "https://w3id.org/ro/crate/1.1/context",
        "https://w3id.org/ro/crate/1.2/context",
    }
    if isinstance(ctx, list):
        if not any(c in allowed for c in ctx if isinstance(c, str)):
            warnings.append("context missing known RO-Crate context (1.1 or 1.2)")
    elif ctx not in allowed:
        warnings.append("context missing known RO-Crate context (1.1 or 1.2)")

    # root dataset
    root = idx.get("./")
    if not root:
        errors.append("metadata.json missing root dataset './'")
        return errors, warnings
    for f in ("name", "description", "license", "resultOf"):
        if f not in root:
            errors.append(f"metadata.json's root dataset missing {f}")
    if not isinstance(root.get("resultOf"), dict) or "@id" not in root["resultOf"]:
        errors.append("root dataset resultOf should point to an @id")

    # flattened additionalProperty
    for ref in root.get("additionalProperty", []):
        if not isinstance(ref, dict) or "@id" not in ref:
            warnings.append("additionalProperty entries should be objects with @id")
            continue
        pv = idx.get(ref["@id"])
        if not pv:
            warnings.append(f"additionalProperty target {ref['@id']} not found")
            continue
        if pv.get("@type") != "PropertyValue":
            warnings.append(f"{ref['@id']}: expected @type PropertyValue")
        if "name" not in pv or "value" not in pv:
            warnings.append(f"{ref['@id']}: PropertyValue missing name or value")

    # acquisition chain
    acq = idx.get(root.get("resultOf", {}).get("@id"))
    if not acq:
        errors.append("resultOf target not found")
        return errors, warnings
    if acq.get("@type") != "image_acquisition":
        errors.append("acquisition missing @type image_acquisition")
    specimen_id = (
        acq.get("specimen", {}).get("@id")
        if isinstance(acq.get("specimen"), dict)
        else None
    )
    specimen = idx.get(specimen_id)
    if not specimen:
        errors.append("specimen not found")
        return errors, warnings
    if specimen.get("@type") != "specimen":
        errors.append("specimen missing @type specimen")
    bios_id = (
        specimen.get("biosample", {}).get("@id")
        if isinstance(specimen.get("biosample"), dict)
        else None
    )
    bios = idx.get(bios_id)
    if not bios:
        errors.append("biosample not found")
    else:
        if bios.get("@type") != "biosample":
            errors.append("biosample missing @type biosample")
        if "organism_classification" not in bios:
            errors.append("biosample missing organism_classification")

    # metadata descriptor
    meta = idx.get("ro-crate-metadata.json")
    if not meta:
        errors.append(
            "metadata json's description of 'ro-crate-metadata.json' in  not found"
        )
    else:
        if meta.get("@type") != "CreativeWork":
            errors.append("metadata descriptor missing @type CreativeWork")
        if meta.get("about", {}).get("@id") != "./":
            errors.append("metadata descriptor about should be './'")
        if (
            not isinstance(meta.get("conformsTo"), dict)
            or "@id" not in meta["conformsTo"]
        ):
            warnings.append(
                "metadata descriptor conformsTo should be an object with @id"
            )

    if "conformsTo" not in root:
        warnings.append("root dataset missing profile conformsTo (SHOULD)")

    return errors, warnings


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Lean RO-Crate sanity check for the local examples."
    )
    default_crate = (
        Path(__file__).resolve().parent
        / "examples"
        / "valid"
        / "example_production_crate.json"
    )
    ap.add_argument("crate", nargs="?", default=str(default_crate))
    args = ap.parse_args()
    data = json.loads(Path(args.crate).read_text(encoding="utf-8"))
    errs, warns = validate(data)
    if warns:
        print("Warnings:")
        for w in warns:
            print(f" - {w}")
    if errs:
        print("Errors:")
        for e in errs:
            print(f" - {e}")
        raise SystemExit(1)
    print("Crate passed minimal checks.")
