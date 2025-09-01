from pydantic import BaseModel

class RequestCreate(BaseModel):
    vin: str
    email: str