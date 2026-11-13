import re

CVE_REGEX: re.Pattern[str] = re.compile(
    r"\b(?P<cve>CVE-(?:1999|20\d{2})-\d{4,})(?![-\w])",
    re.IGNORECASE,
)

GHSA_REGEX: re.Pattern[str] = re.compile(
    r"\b(?P<ghsa>GHSA-[2-9cfghjmpqrvwx]{4}-[2-9cfghjmpqrvwx]{4}-[2-9cfghjmpqrvwx]{4})(?![-\w])",
    re.IGNORECASE,
)

PYSEC_REGEX: re.Pattern[str] = re.compile(
    r"\b(?P<pysec>PYSEC-20\d{2}-[1-9]\d*)(?![-\w])",
    re.IGNORECASE,
)

ADVISORY_PATTERNS: dict[str, re.Pattern[str]] = {
    "CVE": CVE_REGEX,
    "GHSA": GHSA_REGEX,
    "PYSEC": PYSEC_REGEX,
}
