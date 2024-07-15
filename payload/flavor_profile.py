from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Structure:
    acidity: Optional[float]
    fizziness: Optional[float]
    intensity: Optional[float]
    sweetness: Optional[float]
    tannin: Optional[float]=None

@dataclass
class FlavorProfile:
    structure: Structure
    top_flavors: List[str]
