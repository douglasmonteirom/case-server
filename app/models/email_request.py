from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    text: Optional[str] = None
