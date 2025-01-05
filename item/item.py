from pydantic import BaseModel

class Item(BaseModel):
    text: str # Required since no default value
    is_done: bool = False