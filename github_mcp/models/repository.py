from typing import Optional

from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    full_name: str
    private: bool
    description: Optional[str] = None
    url: str
    html_url: str
    owner: str
