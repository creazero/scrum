from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    color: Optional[str]
    project_id: int

    class Config:
        allow_population_by_alias = True
        fields = {
            'project_id': 'projectId'
        }


class TagBaseInDb(TagBase):
    id: int


class TagCreate(TagBase):
    pass


class Tag(TagBaseInDb):
    pass
