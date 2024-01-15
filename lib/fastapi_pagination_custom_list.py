"""
FastAPI Pagination Custom List

Provides a custom pagination class to be used with FastAPI 0.100.0, Pydantic 2.0.2 and SQLAlchemy.

Example of the output JSON:

    {
      "success": true,
      "message": "Success",
      "total": 116135,
      "items": [
        { ... },
      ],
      "page": 1,
      "size": 20,
      "pages": 18
    }

Usage:

    from typing import Annotated

    from fastapi import APIRouter, Depends
    from fastapi_pagination.ext.sqlalchemy import paginate

    from lib.database import Session, get_db
    from lib.exceptions import MyAnyError
    from lib.fastapi_pagination_custom_list import CustomList

    from .crud import get_examples
    from .schemas import AutoridadListOut

    examples = APIRouter(prefix="/v4/examples")

    @examples.get("/listado", response_model=CustomList[AutoridadListOut])
    async def list_examples(
        database: Annotated[Session, Depends(get_db)],
    ):
        try:
            query = get_examples(database=database)
        except MyAnyError as error:
            return CustomList(success=False, message=str(error))
        return paginate(query)

"""
from math import ceil
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.default import Params
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
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
    Custom Page
    """

    success: bool
    message: str

    total: Optional[GreaterEqualZero] = None
    items: Sequence[T] = []
    page: Optional[GreaterEqualOne] = None
    size: Optional[GreaterEqualOne] = None
    pages: Optional[GreaterEqualZero] = None

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
            )

        size = params.size if params.size is not None else total
        page = params.page if params.page is not None else 1
        pages = ceil(total / size) if total is not None else None

        return cls(
            success=True,
            message="Success",
            total=total,
            items=items,
            page=page,
            size=size,
            pages=pages,
            **kwargs,
        )
