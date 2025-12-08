import argparse, json
from pathlib import Path


def validate(crate):
    errors, warnings = [], []
    graph = crate.get("@graph", [])
    idx = {e.get("@id"): e for e in graph if isinstance(e, dict) and "@id" in e}

    # basic context check
    ctx = crate.get("@context")
    base_contexts = {
        "https://w3id.org/ro/crate/1.1/context",
        "https://w3id.org/ro/crate/1.2/context",
    }
    required_terms = {
        "organism_classification": "https://schema.org/taxonomicRange",
        "BioChemEntity": "https://schema.org/BioChemEntity",
        "channel": "https://www.openmicroscopy.org/Schemas/Documentation/Generated/OME-2016-06/ome_xsd.html#Channel",
        "obo": "http://purl.obolibrary.org/obo/",
        "FBcv": "http://ontobee.org/ontology/FBcv/",
        "acquisiton_method": {"@reverse": "https://schema.org/result", "@type": "@id"},
        "biological_entity": "https://schema.org/about",
        "biosample": "http://purl.obolibrary.org/obo/OBI_0002648",
        "preparation_method": "https://www.wikidata.org/wiki/Property:P1537",
        "specimen": "http://purl.obolibrary.org/obo/HSO_0000308",
    }
    base_found = False
    term_mappings = {}
    if isinstance(ctx, list):
        base_found = any(c in base_contexts for c in ctx if isinstance(c, str))
        for c in ctx:
            if isinstance(c, dict):
                term_mappings.update(c)
    elif isinstance(ctx, str):
        base_found = ctx in base_contexts
    else:
        errors.append("@context should be a string or list")

    if not base_found:
        errors.append("context missing required RO-Crate base context (1.1 or 1.2)")
    missing_terms = [k for k, v in required_terms.items() if term_mappings.get(k) != v]
    if missing_terms:
        errors.append(
            "context missing required OME-Zarr term definitions: "
            + ", ".join(missing_terms)
        )

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
