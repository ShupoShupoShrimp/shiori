from typing import Annotated

from fastapi import APIRouter, Body

from shiori.api.schemas.query import UserRequest

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("")
async def ask_question(payload: Annotated[UserRequest, Body()]) -> str:
    # There shall be another return, yet I am testing hypothesis for now...
    return payload.question


# currently under development, since I need to implement some ideas.
