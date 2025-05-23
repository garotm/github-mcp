from typing import List, Optional

from pydantic import BaseModel


class Issue(BaseModel):
    number: int
    title: str
    body: Optional[str] = None
    state: str
    url: str
    labels: List[str] = []
    assignees: List[str] = []
