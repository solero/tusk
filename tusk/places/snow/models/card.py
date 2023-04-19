from pydantic import BaseModel

class PowerCard(BaseModel):
    asset: str = ""
    card_id: int 
    color: str 
    description: str
    element: str
    is_active: bool = True
    label: str
    name: str
    power_id: int
    prompt: str
    set_id: int
    value: int