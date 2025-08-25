from pydantic import BaseModel

class EmailResponse(BaseModel):
    category: str
    suggestion: str
