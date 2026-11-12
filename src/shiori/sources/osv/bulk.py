import io
import logging
import zipfile

import httpx
from pydantic import ValidationError

from shiori.sources.osv.schemas import OSVAdvisory

sea_log = logging.getLogger("security.osv")

PYPI_BULK_URL = "https://osv-vulnerabilities.gcs.googleapis.com/PyPI/all.zip"


class OSVBulkDownloader:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch_and_parse(self, url: str = PYPI_BULK_URL) -> list[OSVAdvisory]:
        response = await self.client.get(url)
        response.raise_for_status()

        advisories: list[OSVAdvisory] = []

        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
            for filename in archive.namelist():
                if filename.endswith(".json"):
                    raw_byte = archive.read(filename)
                    try:
                        advisory = OSVAdvisory.model_validate_json(raw_byte)
                        advisories.append(advisory)
                    except (ValidationError, Exception) as e:
                        sea_log.warning(f"skipping malformed file {filename} due to error: {e}")
                        continue

        return advisories
