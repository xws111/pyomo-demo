from dataclasses import dataclass

from pydantic import BaseModel, Field


class Site(BaseModel):
    code: str = Field(validation_alias='Code')
    name: str = Field(validation_alias='Name')

    def __hash__(self):
        return hash(self.code)


class ModelData(BaseModel):
    origins: list[Site]
    destinations: list[Site]
    supply: dict[str, float]
    demand: dict[str, float]
    cost: dict[tuple[str, str], float]

