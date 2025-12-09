# OME-Zarr RO-Crate Profile 0.1

**Version:** 0.1.0

**RO-Crate version:** `isProfileOf = https://w3id.org/ro/crate/1.1`

**Status:** Draft

This document defines the **OME-Zarr RO-Crate profile**, a minimal RO-Crate convention for OME-Zarr datasets. While not a part of the OME-Zarr spec, this formalizes the use of RO-Crate the context of the **OME 2024 NGFF Challenge** and extends it as a non-normative guideline. 

The goal of the profile is to enable individuals generating OME-Zarr data to: 

* add licensing information to the dataset
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
  { "@id": "https://github.com/lubianat/ome-zarr-ro-crate/crate/tree/0.0.1/profile" }
]
```

---

### 2.2 Root Data Entity (`"./"`)

The Root Dataset **MUST**:

* have `@type` including `"Dataset"`;
* specify `name`, `description`, and `license`;
* refer via `resultOf` to **exactly one** `image_acquisition` entity.

Additionally, it **MUST** specify `conformsTo` including this profile’s URI (production crates currently omit this).

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
* declare RO-Crate specification conformance to RO-Crate 1.2

```json
"conformsTo": { "@id": "https://w3id.org/ro/crate/1.2" }
```

---

### 2.4 Required JSON-LD Context

Every conforming crate **MUST**:

1. include the RO-Crate base context `https://w3id.org/ro/crate/1.2/context`; 
2. 
Crates **MAY** include additional context entries (extra URLs or term maps) to carry arbitrary Linked Open Data; these do not affect conformance as long as the required base context and terms above are present.

Optional example terms (not required for conformance; you may include any other terms you need):

```json
{
  "BioChemEntity": "https://schema.org/BioChemEntity",
  "channel": "https://www.openmicroscopy.org/Schemas/Documentation/Generated/OME-2016-06/ome_xsd.html#Channel",
  "FBcv": "http://ontobee.org/ontology/FBcv/",
  "preparation_method": "https://www.wikidata.org/wiki/Property:P1537",
  "obo": "http://purl.obolibrary.org/obo/",
  "acquisiton_method": {
    "@reverse": "https://schema.org/result",
    "@type": "@id"
  },
  "biological_entity": "https://schema.org/about",

}
```

Example (1.2 base context plus an optional imaging-oriented block):

```json
"@context": [
  "https://w3id.org/ro/crate/1.2/context",
  {
    "organism_classification": "https://schema.org/taxonomicRange",
    "obo": "http://purl.obolibrary.org/obo/",
    "biological_entity": "https://schema.org/about",
  }
]
```

The optional block above is illustrative only; include any additional contexts/terms you need for your data.

---

## 3. Required Entities

### 3.1 OME-Zarr File Entities

The crate **MUST** define a RO-Crate `Dataset`:

Example:

```json
{
  "@id": "./",
  "@type": "Dataset",
  "name": "Example OME-Zarr dataset",
  "description": "Converted for the OME 2024 NGFF Challenge",
  "license": "https://creativecommons.org/licenses/by/4.0/",
}
```

(non normative)
The ro-crate-metadata.json document may be in the .zarr root (as an attached ro-crate). \

If it is provided independently, it MAY work as a detached RO-Crate by providing a Zarr url, for example: 

(from https://github.com/NFDI4BIOIMAGE/FAIR-IO/pull/1/files#diff-6b65cda33d25cfaa5b3695218f93f221e7c56c526cc5f639e1927d38221e4047)

```json
    "@graph": [
      {
        "@id": "https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD464",
        "@type": "Dataset",
        "name": "Calcium wave dynamics",
        "description": "Time lapse image of whole leaves expressing calcium and glutamate responses",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "hasPart":{"@id":"https://uk1s3.embassy.ebi.ac.uk/ebi-ngff-challenge-2024/c0e5d621-62cc-43a6-9dad-2ddab8959d17.zarr/zarr.json"}
      }
```

### 3.1 Arbitrary key/value metadata

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

If richer semantics are needed, producers may add use `@context` and URIs to provide ontology terms to the key value pairs.

```json
{
  "@id": "#acq-001",
  "name": "image_acquisition_method",
  "fbbi_id": {
    "@id": "obo:FBbi_00000369"
  }
}
```

```json
{
  "@id": "#bios-001",
  "name": "taxon", 
  "value": {
    "@id": "http://purl.obolibrary.org/obo/NCBITaxon_9606"
  }
}
```

Acceptable organism values include those provided by `ome2024-ngff-challenge --rocrate-organism` (e.g., `NCBI:txid9606`), which SHOULD be normalized by the profile context to resolvable URIs.


---

## 4. Alignment with the OME 2024 NGFF Challenge

For more details, see the OME 2024 NGFF Challenge repository: [https://github.com/ome/ome2024-ngff-challenge](https://github.com/ome/ome2024-ngff-challenge)

This version of the crate uses a different, more minimal modelling in comparison to the OME Challenge tool (`ome2024-ngff-challenge`).

In particular, it does not enforce a model for samples or for the image acquisition method.