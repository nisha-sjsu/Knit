from pydantic import BaseModel

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