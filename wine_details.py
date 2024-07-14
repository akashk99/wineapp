from dataclasses import dataclass
from typing import Optional

from wine import Wine


@dataclass
class WineDetails:
    name: str
    region: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    reviews: Optional[str] = None