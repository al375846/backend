from pydantic import BaseModel

class BasicReturn(BaseModel):
    done:bool = True