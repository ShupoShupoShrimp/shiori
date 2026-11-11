from pydantic import BaseModel, ConfigDict

# ------------------------------------------------------------------------------
# Sub-Models & Components
# ------------------------------------------------------------------------------


class OSVEvents(BaseModel):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVRange(BaseModel):
    type: str
    repo: str | None = None
    events: list[OSVEvents] = []

    model_config = ConfigDict(extra="ignore")


class OSVPackage(BaseModel):
    name: str
    ecosystem: str
    purl: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVEcosystemSpecific(BaseModel):
    severity: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVDatabaseSpecific(BaseModel):
    source: str | None = None

    model_config = ConfigDict(extra="ignore")


class OSVRangeAffected(BaseModel):
    package: OSVPackage | None = None
    ranges: list[OSVRange] = []
    versions: list[str] = []
    ecosystem_specific: OSVEcosystemSpecific | None = None
    database_specific: OSVDatabaseSpecific | None = None

    model_config = ConfigDict(extra="ignore")


class OSVReferences(BaseModel):
    type: str
    url: str

    model_config = ConfigDict(extra="ignore")


# ------------------------------------------------------------------------------
# Endpoint Response Models
# ------------------------------------------------------------------------------

# ------------------ GET /v1/vulns/{id} ------------------


class OSVAdvisory(BaseModel):
    id: str
    summary: str | None = None
    details: str | None = None
    modified: str | None = None
    published: str | None = None
    references: list[OSVReferences] = []
    affected: list[OSVRangeAffected] | None = None
    schema_version: str | None = None

    model_config = ConfigDict(extra="ignore")


# ------------------ POST /v1/query ------------------


class OSVQueryResponse(BaseModel):
    vulns: list[OSVAdvisory] = []

    model_config = ConfigDict(extra="ignore")
