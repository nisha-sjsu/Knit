from typing import Dict
from pydantic import BaseModel
from datetime import datetime

# Properties to send to Flipt
class EvaluationRequest(BaseModel):
    key_name: str
    request_id: str

# Model for the response from Flipt and the outgoing response to the client
class EvaluationResponse(BaseModel):
    key_name: str
    request_id: str
    enabled: bool
    reason: str

class RequestContext(BaseModel):
    user_agent: str

class FliptPayload(BaseModel):
    flagKey: str
    entityId: str
    context: RequestContext

class FliptData(BaseModel):
    enabled: bool
    reason: str
    requestId: str
    requestDurationMillis: float
    timestamp: datetime
    flagKey: str