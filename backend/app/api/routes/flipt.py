from fastapi import APIRouter, Request, Header
import httpx
from models import EvaluationRequest, EvaluationResponse, FliptPayload, FliptData, RequestContext

router = APIRouter()


@router.post("/evaluate/boolean", response_model=EvaluationResponse)
async def evaluate_boolean(evaluation_request: EvaluationRequest, request: Request, useragent: str = Header(...)):
    
    # payload for Flipt
    flipt_payload = FliptPayload(flagKey = evaluation_request.key_name,
        entityId = evaluation_request.request_id,
        context = RequestContext(user_agent=useragent))

    # async request to Flipt server
    async with httpx.AsyncClient() as client:
        flipt_response = await client.post(
            "http://flipt-server:8080/evaluate/v1/boolean",
            json=flipt_payload.model_dump()
        )
    
    flipt_data = FliptData( **flipt_response.json() )

    # final response
    return EvaluationResponse(
        key_name=evaluation_request.key_name,
        request_id=evaluation_request.request_id,
        enabled=flipt_data.enabled,
        reason=flipt_data.reason 
    )