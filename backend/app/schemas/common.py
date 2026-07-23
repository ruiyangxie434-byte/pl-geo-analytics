from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool = True
    message: str
    data: DataT | None = None


class ErrorItem(BaseModel):
    field: str | None = None
    message: str
    type: str | None = None


class ErrorResponse(BaseModel):
    success: Literal[False] = False
    message: str
    data: None = None
    errors: list[ErrorItem] | None = None
