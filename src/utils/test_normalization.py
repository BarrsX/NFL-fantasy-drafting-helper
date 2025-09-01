import re


def normalize_player_name(name):
    """Normalize player names by removing common suffixes and standardizing format."""
    if not isinstance(name, str):
        return name

    # Convert to title case for consistency
    name = name.strip().title()

    # Remove common suffixes (Jr., Sr., II, III, etc.)
    suffixes = [
        " Jr.",
        " Sr.",
        " II",
        " III",
        " IV",
        " V",
        " Jr",
        " Sr",
        " Ii",
        " Iii",
        " Iv",
        " V",
        " Jr.",
        " Sr.",
        " Ii.",
        " Iii.",
        " Iv.",
        " V.",
    ]

    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[: -len(suffix)].strip()
            break

    # Handle other common name variations
    # Remove apostrophes (Ja'Marr -> JaMarr, De'Von -> DeVon)
    name = name.replace("'", "")

    # Remove periods (A.J. -> AJ, C.J. -> CJ)
    name = name.replace(".", "")

    # Standardize hyphens (Amon-Ra -> AmonRa, Jaxon Smith-Njigba -> Jaxon SmithNjigba)
    name = name.replace("-", "")

    # Remove extra spaces and normalize spacing
    name = re.sub(r"\s+", " ", name).strip()

    return name


# Test the function with various name formats
test_names = [
    "Ja'Marr Chase",
    "A.J. Brown",
    "Amon-Ra St. Brown",
    "TreVeyon Henderson",
    "DeVonta Smith",
    "D'Andre Swift",
    "C.J. Stroud",
    "T.J. Hockenson",
    "Marvin Harrison Jr.",
    "Kyle Pitts Sr.",
    "Patrick Mahomes II",
    "Deebo Samuel Sr.",
    "Jaxon Smith-Njigba",
    "De'Von Achane",
]

print("Testing enhanced name normalization:")
print("=" * 50)
for name in test_names:
    normalized = normalize_player_name(name)
    print(f"{name:<25} -> {normalized}")
