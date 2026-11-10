from typing import Annotated

from fastapi import APIRouter, Body

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("")
async def ask_question(question: Annotated[str, Body()]) -> str:
    # There shall be another return, yet I am testing hypothesis for now...
    return question


# currently under development, since I need to implement some ideas.
