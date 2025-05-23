from typing import Optional

from pydantic import BaseModel


class PullRequest(BaseModel):
    number: int
    title: str
    body: Optional[str] = None
    state: str
    url: str
    head: str
    base: str
    draft: Optional[bool] = False
