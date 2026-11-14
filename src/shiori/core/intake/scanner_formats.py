from shiori.core.intake.models import ExtractedIdentifiers
from shiori.core.intake.patterns import ADVISORY_PATTERNS


def parse_prompt(message: str) -> ExtractedIdentifiers:
    extracted: dict[str, set[str]] = {
        "cve_ids": set(),
        "ghsa_ids": set(),
        "pysec_ids": set(),
    }
    for advisory_type, pattern in ADVISORY_PATTERNS.items():
        adv_type = f"{advisory_type.lower()}_ids"
        if adv_type not in extracted:
            continue

        for match in pattern.finditer(message):
            val = match.group(advisory_type.lower()) if advisory_type.lower() in match.groupdict() else match.group()
            extracted[adv_type].add(val)

    return ExtractedIdentifiers(
        cve_ids=list(extracted["cve_ids"]),
        ghsa_ids=list(extracted["ghsa_ids"]),
        pysec_ids=list(extracted["pysec_ids"]),
    )
