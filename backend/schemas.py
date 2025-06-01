from typing import Optional
from pydantic import BaseModel

class Transfer(BaseModel):
    transfer_id: str
    status: str  #"official", "rumor", "loan", or None
    player_name: str
    from_club: Optional[str] = None
    to_club: Optional[str] = None
    transfer_amount: Optional[float] = None
    position: Optional[str] = None