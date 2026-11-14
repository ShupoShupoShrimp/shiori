from pydantic import BaseModel, Field


class ExtractedIdentifiers(BaseModel):
    cve_ids: list[str] = Field(default_factory=list)
    ghsa_ids: list[str] = Field(default_factory=list)
    pysec_ids: list[str] = Field(default_factory=list)
