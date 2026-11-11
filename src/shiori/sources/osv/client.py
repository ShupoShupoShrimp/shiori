import httpx

from shiori.sources.osv.schemas import OSVAdvisory, OSVQueryResponse

OSV_VULNS_URL = "https://api.osv.dev/v1/vulns"
OSV_QUERY_URL = "https://api.osv.dev/v1/query"


async def advisory_search(vuln_id: str) -> OSVAdvisory:

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OSV_VULNS_URL}/{vuln_id}")

        response.raise_for_status()
        return OSVAdvisory.model_validate(response.json())


async def commit_query_search(commit: str) -> OSVQueryResponse:

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=OSV_QUERY_URL,
            json={"commit": commit},
        )

        response.raise_for_status()
        return OSVQueryResponse.model_validate(response.json())


async def package_query_search(name: str, ecosystem: str, version: str) -> OSVQueryResponse:
    async with httpx.AsyncClient() as client:
        response = await client.post(
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


# Still making some hypothesis.
