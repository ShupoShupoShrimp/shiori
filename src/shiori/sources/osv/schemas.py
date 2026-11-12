from typing import Any

from pydantic import BaseModel, ConfigDict

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# OPEN SOURCE VULNERABILITIES
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Sub-Models & Components
# ------------------------------------------------------------------------------


class OSVEvents(BaseModel):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None
    limit: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVRange(BaseModel):
    type: str
    repo: str | None = None
    events: list[OSVEvents] = []
    database_specific: dict[str, Any] | None = None

    model_config = ConfigDict(extra="ignore")


class OSVPackage(BaseModel):
    ecosystem: str
    name: str
    purl: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVSeverity(BaseModel):
    type: str | None = None
    score: str | None = None
    source: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVRangeAffected(BaseModel):
    package: OSVPackage | None = None
    severity: list[OSVSeverity] = []
    ranges: list[OSVRange] = []
    versions: list[str] = []
    ecosystem_specific: dict[str, Any] | None = None
    database_specific: dict[str, Any] | None = None

    model_config = ConfigDict(extra="ignore")


class OSVReferences(BaseModel):
    type: str
    url: str

    model_config = ConfigDict(extra="ignore")


class OSVCredits(BaseModel):
    name: str
    contact: list[str] = []
    type: str | None = None

    model_config = ConfigDict(extra="ignore")


# ------------------------------------------------------------------------------
# Endpoint Response Models
# ------------------------------------------------------------------------------


class OSVAdvisory(BaseModel):
    schema_version: str | None = None
    id: str
    modified: str
    published: str | None = None
    withdrawn: str | None = None
    aliases: list[str] = []
    upstream: list[str] = []
    related: list[str] = []
    summary: str | None = None
    details: str | None = None
    severity: list[OSVSeverity] = []
    affected: list[OSVRangeAffected] = []
    references: list[OSVReferences] = []
    credits: list[OSVCredits] = []
    database_specific: dict[str, Any] | None = None

    model_config = ConfigDict(extra="ignore")


# ------------------ POST /v1/query ------------------


class OSVQueryResponse(BaseModel):
    vulns: list[OSVAdvisory] = []

    model_config = ConfigDict(extra="ignore")
