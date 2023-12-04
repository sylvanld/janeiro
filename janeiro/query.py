from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

DEFAULT_PAGE_LIMIT = 20

T = TypeVar("T")


class Pagination(BaseModel):
    page: int
    limit: int


class Paginated(BaseModel, Generic[T]):
    page: int = 0
    limit: int = DEFAULT_PAGE_LIMIT
    size: int = 0
    total: int = 0
    results: List[T] = Field(default_factory=list)
