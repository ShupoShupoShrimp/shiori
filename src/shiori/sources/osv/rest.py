import httpx

from shiori.sources.osv.schemas import OSVAdvisory, OSVQueryResponse

OSV_VULNS_URL = "https://api.osv.dev/v1/vulns"
OSV_QUERY_URL = "https://api.osv.dev/v1/query"


class OSVClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def advisory_search(self, vuln_id: str) -> OSVAdvisory:

        response = await self.client.get(f"{OSV_VULNS_URL}/{vuln_id}")

        response.raise_for_status()
        return OSVAdvisory.model_validate(response.json())

    async def commit_query_search(self, commit: str) -> OSVQueryResponse:

        response = await self.client.post(
            url=OSV_QUERY_URL,
            json={"commit": commit},
        )

        response.raise_for_status()
        return OSVQueryResponse.model_validate(response.json())

    async def package_query_search(self, name: str, ecosystem: str, version: str) -> OSVQueryResponse:
        response = await self.client.post(
            url=OSV_QUERY_URL,
            json={
                "package": {
                    "name": name,
                    "ecosystem": ecosystem,
                },
                "version": version,
            },
        )

        response.raise_for_status()
        return OSVQueryResponse.model_validate(response.json())
