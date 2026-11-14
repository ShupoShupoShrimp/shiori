from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, UniqueConstraint, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shiori.db.base import Base
from dataclasses import dataclass

class AdvisoryDB(Base):
    __tablename__ = "advisories"

    id: Mapped[int] = mapped_column(primary_key=True)

    source_name: Mapped[str] = mapped_column(String)
    advisory_id: Mapped[str] = mapped_column(String)

    modified: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )
    published: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )
    withdrawn: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )

    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON)

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    osv_advisory: Mapped["OSVAdvisory | None"] = relationship(
        back_populates="advisory",
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("source_name", "advisory_id"),)


@dataclass
class IncomingAdvisory:
    source_name: str
    advisory_id: str
    modified: datetime | None
    published: datetime | None
    withdrawn: datetime | None
    raw_payload: dict[str, Any]
    data: Any

@dataclass
class AdvisoryIngestionResult:
    processed: int = 0
    new: int = 0
    unchanged: int = 0
    modified: int = 0
    failed: int = 0

class IngestionAction(str, Enum):
    NEW = "NEW"
    UNCHANGED = "UNCHANGED"
    MODIFIED = "MODIFIED"

class OSVAdvisory(Base):
    __tablename__ = "osv_advisories"

    id: Mapped[int] = mapped_column(primary_key=True)

    advisory_record_id: Mapped[int] = mapped_column(
        ForeignKey("advisories.id"),
        unique=True,
    )

    schema_version: Mapped[str | None] = mapped_column(
        String,
        default=None,
    )

    advisory: Mapped["Advisory"] = relationship(
        back_populates="osv_advisory",
    )

    affected: Mapped[list["OSVAffectedSQL"]] = relationship(
        back_populates="osv_advisory",
        cascade="all, delete-orphan",
    )


class OSVAffectedSQL(Base):
    __tablename__ = "osv_affected"

    id: Mapped[int] = mapped_column(primary_key=True)

    osv_advisory_id: Mapped[int] = mapped_column(
        ForeignKey("osv_advisories.id"),
    )

    osv_advisory: Mapped["OSVAdvisory"] = relationship(
        back_populates="affected",
    )

    package: Mapped["OSVPackageSQL"] = relationship(
        back_populates="affected",
        cascade="all, delete-orphan",
    )

    severity: Mapped[list["OSVSeveritySQL"]] = relationship(
        back_populates="affected",
        cascade="all, delete-orphan",
    )

    ranges: Mapped[list["OSVRangeSQL"]] = relationship(
        back_populates="affected",
        cascade="all, delete-orphan",
    )

    versions: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
    )

    ecosystem_specific: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        default=None,
    )

    database_specific: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        default=None,
    )


class OSVPackageSQL(Base):
    __tablename__ = "osv_affected_packages"

    id: Mapped[int] = mapped_column(primary_key=True)

    affected_id: Mapped[int] = mapped_column(
        ForeignKey("osv_affected.id"),
        unique=True,
    )

    ecosystem: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    purl: Mapped[str | None] = mapped_column(String, default=None)

    affected: Mapped["OSVAffectedSQL"] = relationship(
        back_populates="package",
    )


class OSVSeveritySQL(Base):
    __tablename__ = "osv_affected_severity"

    id: Mapped[int] = mapped_column(primary_key=True)

    affected_id: Mapped[int] = mapped_column(
        ForeignKey("osv_affected.id"),
    )

    type: Mapped[str] = mapped_column(String)
    score: Mapped[str] = mapped_column(String)
    source: Mapped[str | None] = mapped_column(String, default=None)

    affected: Mapped["OSVAffectedSQL"] = relationship(
        back_populates="severity",
    )


class OSVRangeSQL(Base):
    __tablename__ = "osv_affected_ranges"

    id: Mapped[int] = mapped_column(primary_key=True)

    affected_id: Mapped[int] = mapped_column(
        ForeignKey("osv_affected.id"),
    )

    type: Mapped[str] = mapped_column(String)
    repo: Mapped[str | None] = mapped_column(String, default=None)

    events: Mapped[list["OSVEventSQL"]] = relationship(
        back_populates="range",
        cascade="all, delete-orphan",
    )

    database_specific: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        default=None,
    )

    affected: Mapped["OSVAffectedSQL"] = relationship(
        back_populates="ranges",
    )


class OSVEventSQL(Base):
    __tablename__ = "osv_affected_range_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    range_id: Mapped[int] = mapped_column(
        ForeignKey("osv_affected_ranges.id"),
    )

    event_type: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    range: Mapped["OSVRangeSQL"] = relationship(
        back_populates="events",
    )
