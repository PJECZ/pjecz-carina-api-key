"""
FastAPI Pagination Custom Page - Materias
"""
from abc import ABC
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from typing_extensions import Self

from lib.fastapi_pagination_custom_page import CustomPageParams

T = TypeVar("T")


class MateriasCustomPage(AbstractPage[T], Generic[T], ABC):
    """
    Custom Page
    """

    success: bool
    message: str

    total: Optional[GreaterEqualZero] = None
    materias: Sequence[T] = []
    limit: Optional[GreaterEqualOne] = None
    offset: Optional[GreaterEqualZero] = None

    __params_type__ = CustomPageParams

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
        raw_params = params.to_raw_params().as_limit_offset()

        if total is None or total == 0:
            return cls(
                success=True,
                message="No se encontraron registros",
            )

        return cls(
            success=True,
            message="Success",
            total=total,
            materias=items,
            limit=raw_params.limit,
            offset=raw_params.offset,
            **kwargs,
        )
