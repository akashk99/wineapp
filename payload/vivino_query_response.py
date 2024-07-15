from dataclasses import dataclass
from typing import Optional


@dataclass
class VivinoQueryResponse:
    name: str
    vintage_id: int
    alcohol_content: Optional[float] = None
    menu_price: Optional[float] = None
    menu_year: Optional[float] = None
    online_price: Optional[int] = None
    region: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    reviews: Optional[str] = None