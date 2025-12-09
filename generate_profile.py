from rocratepcc import *

# List all types which are used in this profile
types = [
    UsedType(iri="https://schema.org/CreativeWork", name="CreativeWork"),
    UsedType(iri="http://www.w3.org/ns/dx/prof/Profile", name="Profile"),
]

# List all authors of this profile
authors = [Author(name="Tiago Lubiana", orcid="0000-0003-2473-2313")]

# Version of the profile (semver if possible)
version = "0.0.1dev"

# Identifier of the root data entity of the profile, if url not applicable then use "./"
id = f"https://github.com/lubianat/ome-zarr-ro-crate/crate/tree/{version}/profile"

# Name of the profile
name = "Experimental OME-Zarr minimal RO-Crate Profile"

# Description of the profile

description = "An RO-Crate profile for representing OME-Zarr data in Research Object Crates (RO-Crates). "

# License by which the profile is published
license = License(iri="https://mit-license.org/", name="MIT License")

# List of the textual resources we use as specifications for this profile
specifications = [
    TextualResource(
        name="OME-Zarr RO-Crate Profile description",
        file_path="index.md",
        encoding_format="text/markdown",
        root_data_entity_id=id,
    )
]

# List of all the resource descriptors. Here, only the specification is given.
resourceDescriptors = [
    Specification(specifications)
    # Example()
    # Guidance()
    # Constraint()
]

# The root data entity of the profile
rootEntity = RootDataEntity(
    id=id,
    name=name,
    description=description,
    license=license,
    used_types=types,
    resource_descriptors=resourceDescriptors,
    authors=authors,
)

# Profile entity
profile = Profile(rootEntity, license=license)

# Convert the profile to a JSON-LD string
string = profile.ToROCrateJsonString(spaces=2)

# Write the string to a file "ro-crate-metadata.json"
with open("ro-crate-metadata.json", "w", encoding="utf-8") as f:
    f.write(string)
