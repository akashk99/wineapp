from dataclasses import dataclass
from typing import Optional

from winemenuitem import WineMenuItem


@dataclass
class WineDetails:
    name: str
    menu_price: Optional[int] = None
    menu_year: Optional[int] = None
    online_price: Optional[int] = None
    region: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    reviews: Optional[str] = None