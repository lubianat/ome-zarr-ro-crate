# OME-Zarr RO-Crate Profile 0.1

**Version:** 0.1.0

**RO-Crate version:** `isProfileOf = https://w3id.org/ro/crate/1.1`

**Status:** Draft

This document defines the **OME-Zarr RO-Crate profile**, a minimal RO-Crate convention for OME-Zarr datasets. While not a part of the OME-Zarr spec, this formalizes the use of RO-Crate the context of the **OME 2024 NGFF Challenge** and extends it as a non-normative guideline. 

The goal of the profile is to enable individuals generating OME-Zarr data to: 

* add licensing information to the dataset
* add basic information for searching, namely the imaging modality and the species studied
* support arbitrary metadata to be packed in OME-Zarr files

The profile is agnostic to OME-Zarr versions and should be compatible with any, as long as it is provided in the root of the Zarr hierarchy. 

RFC-9 compatible datasets ("zip zarrs" or Zipped OME-Zarrs) may include a ro-crate-metadata.json file, as non-zipped Zarrs can.

## 1. Introduction

As not everyone is used to the Linked Data jargon and the JSON-LD details, as well as the RO-Crate model, this introduction/glossary was conceived. If you are unfamiliar with JSON-LD, for example, [this video](https://www.youtube.com/watch?v=vioCbTo3C-4) may be a good place to start.  

* **RO-Crate**: a combination of data files originated in scientific research AND a metadata file called `ro-crate-metadata.json`. The metadata is written in JSON-LD and follows some rules, which are refined by this Profile.

* **Root Data Entity**: in OME-Zarr files, this logical JSON-LD entity refers to the data as a whole, pointing to the root directory including the OME-Zarr `zarr.json` metadata. As OME-Zarr is already a multi-folder format, the `ro-crate-metadata.json` is put directly *inside* the file.

* **@type**, **@context**, **@id** and **@graph** etc.: fields preceded by "@" are special keywords in JSON-LD that make JSON files "semantic" in the Semantic Web sense. They disambiguate concepts and are boilerplate for some applications. 

* **@id**: As RO-Crates use *flattened* JSON-LD, everything gets an **@id** field. It may be a string or a URI. If it looks like a string in JSON-LD, it is actually using the **@context** under the hood to create URIs. For example:

```
{
  "@id": "./",
  "@type": "Dataset",
  "name": "141-Sato-CellMorphology/Fig3a_FIB-SEM_synapse",
  "resultOf": {
    "@id": "#368f5e92-93c4-43b6-a795-00f366656519"
  }
},
{
  "@id": "#368f5e92-93c4-43b6-a795-00f366656519",
  "@type": "image_acquisition",
  "fbbi_id": {
    "@id": "obo:FBbi_00050000"
  }
}
```

This flattened JSON-LD uses hash-generated IDs to be semantically equivalent to the nested structure:

```
{
  "@id": "./",
  "@type": "Dataset",
  "name": "141-Sato-CellMorphology/Fig3a_FIB-SEM_synapse",
  "resultOf": {
    "@type": "image_acquisition",
    "fbbi_id": {
      "@id": "obo:FBbi_00050000"
    }
  }
}
```

---

## 2. Conformance

A crate conforming to the **OME-Zarr RO-Crate Profile**:

### 2.1 RO-Crate validity

1. **MUST** be a valid RO-Crate, conforming to either the 1.1 or 1.2 specification.
2. **SHOULD** declare conformance of the [Root Data Entity](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity.html) ("./") to the profile in `ro-crate-metadata.json`.

Example:

```json
"conformsTo": [
  { "@id": "https://github.com/lubianat/ozx_ro_crate/crate/tree/0.0.1/profile" }
]
```

---

### 2.2 Root Data Entity (`"./"`)

The Root Dataset **MUST**:

* have `@type` including `"Dataset"`;
* specify `name`, `description`, and `license`;
* refer via `resultOf` to **exactly one** `image_acquisition` entity.

Additionally, it **SHOULD** specify `conformsTo` including this profile’s URI (production crates currently omit this).

Example:

```json
{
  "@id": "./",
  "@type": "Dataset",
  "name": "Example OME-Zarr dataset",
  "description": "Converted for the OME 2024 NGFF Challenge",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "resultOf": { "@id": "#acq-001" }
}
```

---

### 2.3 RO-Crate Metadata Descriptor (`"ro-crate-metadata.json"`)

This entity **MUST**:

* have `@type` including `"CreativeWork"`;
* have `"about": {"@id": "./"}`;
* declare RO-Crate specification conformance:

```json
"conformsTo": { "@id": "https://w3id.org/ro/crate/1.1" }
```

---

### 2.4 Required JSON-LD Context

Every conforming crate **MUST** use this context form (matching the production crates):

```json
"@context": [
  "https://w3id.org/ro/crate/1.1/context",
  {
    "organism_classification": "https://schema.org/taxonomicRange",
    "BioChemEntity": "https://schema.org/BioChemEntity",
    "channel": "https://www.openmicroscopy.org/Schemas/Documentation/Generated/OME-2016-06/ome_xsd.html#Channel",
    "obo": "http://purl.obolibrary.org/obo/",
    "FBcv": "http://ontobee.org/ontology/FBcv/",
    "acquisiton_method": {
      "@reverse": "https://schema.org/result",
      "@type": "@id"
    },
    "biological_entity": "https://schema.org/about",
    "biosample": "http://purl.obolibrary.org/obo/OBI_0002648",
    "preparation_method": "https://www.wikidata.org/wiki/Property:P1537",
    "specimen": "http://purl.obolibrary.org/obo/HSO_0000308"
  }
]
```

The second context **defines compact terms** for:

* organism taxon (NCBI Taxon IDs),
* FBbi imaging modality (`fbbi_id` on the acquisition),
* specimen and biosample structure,
* additional useful imaging-related terms.

---

## 3. Required Entities

The OME-Zarr RO-Crate profile defines a **minimal biological chain**:

```
Root Dataset
 └─ resultOf → image_acquisition
    └─ specimen → Specimen
       └─ biosample → Biosample
          └─ organism_classification → NCBI Taxon
```

### 3.1 OME-Zarr File Entities

The crate **SHOULD** define the Zarr group(s) as RO-Crate `Dataset`:

Example:

```json
{
  "@id": "./",
  "@type": "Dataset",
  "name": "Example OME-Zarr dataset",
  "description": "Converted for the OME 2024 NGFF Challenge",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "resultOf": { "@id": "#acq-001" }
}
```

### 3.2 ImageAcquisition Entity

Represents the imaging modality and link to the specimen.

```json
{
  "@id": "#acq-001",
  "@type": "image_acquisition",
  "specimen": { "@id": "#spec-001" },
  "fbbi_id": {
    "@id": "obo:FBbi_00000369"
  }
}
```

### 3.3 Specimen Entity

If present, a specimen **MUST** refer to exactly one biosample.

```json
{
  "@id": "#spec-001",
  "@type": "specimen",
  "biosample": { "@id": "#bios-001" }
}
```

### 3.4 Biosample Entity


```json
{
  "@id": "#bios-001",
  "@type": "biosample",
  "organism_classification": {
    "@id": "http://purl.obolibrary.org/obo/NCBITaxon_9606"
  }
}
```

Acceptable organism values include those provided by `ome2024-ngff-challenge --rocrate-organism` (e.g., `NCBI:txid9606`), which SHOULD be normalized by the profile context to resolvable URIs.

---

### 3.5 Arbitrary key/value metadata

RO-Crates use a **flattened JSON-LD graph**, so extra metadata should be added on the relevant entity as additional predicates. For simple key/value pairs (e.g., collection date, experimental treatment), crates **MAY** use Schema.org `additionalProperty` with `PropertyValue` while keeping the existing `@context` unchanged. In flattened JSON-LD, each thing gets an `@id` and appears as its own object in `@graph`:

```json
[
  {
    "@id": "./",
    "@type": "Dataset",
    "name": "Example OME-Zarr dataset",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "resultOf": { "@id": "#acq-001" },
    "additionalProperty": [ { "@id": "#ap-collection" }, { "@id": "#ap-treatment" } ]
  },
  {
    "@id": "#ap-collection",
    "@type": "PropertyValue",
    "name": "collection_date",
    "value": "2024-02-11"
  },
  {
    "@id": "#ap-treatment",
    "@type": "PropertyValue",
    "name": "experimental_treatment",
    "value": "DMSO control"
  }
]
```

If richer semantics are needed, producers MAY extend `@context` with compact terms and use them directly as properties on flattened entities, but simple key/value usage via `additionalProperty` is preferred for interoperability.

---

## 4. Alignment with the OME 2024 NGFF Challenge

For more details, see the OME 2024 NGFF Challenge repository: [https://github.com/ome/ome2024-ngff-challenge](https://github.com/ome/ome2024-ngff-challenge)

The OME Challenge tool (`ome2024-ngff-challenge`) already emits:

* `--rocrate-name` → mapped to Dataset `name`;
* `--rocrate-description` → mapped to Dataset `description`;
* `--rocrate-organism` → mapped to Biosample `organism_classification`;
* `--rocrate-modality` → mapped to Acquisition `fbbi_id`;
* `--cc-by` / `--cc0` / explicit license → mapped to Dataset `license`.

This profile **formalizes** the relationships and required entity graph so the challenge metadata becomes **interoperable RO-Crate**.
