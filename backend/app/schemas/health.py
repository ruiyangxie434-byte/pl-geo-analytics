from typing import Literal

from pydantic import BaseModel


class HealthData(BaseModel):
    service: str
    status: Literal["healthy"]
    environment: str
    version: str
