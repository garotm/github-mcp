from typing import Optional

from pydantic import BaseModel


class FileContent(BaseModel):
    path: str
    content: str
    encoding: str
    size: Optional[int] = None
    sha: Optional[str] = None
    url: Optional[str] = None
