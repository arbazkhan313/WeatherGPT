from fastapi import APIRouter, HTTPException, Query

from app.agents.orchestrator import WeatherOrchestrator


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)

orchestrator = WeatherOrchestrator()


@router.get("/ask")
async def ask_agent(
    question: str = Query(..., description="Your weather question")
):
    try:
        result = await orchestrator.process(question)

        return result

    except Exception as e:
        print("AGENT ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
