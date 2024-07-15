from dataclasses import dataclass
from typing import Optional

from payload.flavor_profile import FlavorProfile


@dataclass
class WineDetails:
    name: str
    menu_price: Optional[int] = None
    flavor_profile: Optional[FlavorProfile] = None
    alcohol_content: Optional[float] = None
    menu_year: Optional[int] = None
    online_price: Optional[int] = None
    region: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    reviews: Optional[str] = None