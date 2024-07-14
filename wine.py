from dataclasses import dataclass
import json
from typing import List, Optional


@dataclass
class Wine:
    name: str
    year: Optional[int]
    price: Optional[float]