from dataclasses import dataclass
import json
from typing import List, Optional


@dataclass
class WineMenuItem:
    name: str
    year: Optional[int]
    price: Optional[float]