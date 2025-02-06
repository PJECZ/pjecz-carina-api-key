"""
FastAPI Pagination Custom List
"""

from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.default import Params
from typing_extensions import Self


class CustomListParams(Params):
    """
    Custom Page Params
    """

    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(500, ge=1, le=1000, description="Page size")


T = TypeVar("T")


class CustomList(AbstractPage[T], Generic[T]):
    """
    Custom List
    """

    success: bool
    message: str
    errors: list[str]
    data: Sequence[T] | None

    __params_type__ = CustomListParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Self:
        """
        Create Custom Page
        """
        if not isinstance(params, Params):
            raise TypeError("Page should be used with Params")

        if total is None or total == 0:
            return cls(
                success=True,
                message="No se encontraron registros",
                errors=[],
                data=[],
            )

        return cls(
            success=True,
            message="Success",
            errors=[],
            data=items,
            **kwargs,
        )
