from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from common.crud import Crud
from common.exceptions import DoesNotExist
from common.urls import Urls


class Model(BaseModel):
    class Meta:
        collection: str
        url: str

    pk: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @classmethod
    def crud(cls) -> Crud:
        return Crud(cls.Meta.collection, cls)

    @classmethod
    def urls(cls) -> Urls:
        return Urls(cls.crud())

    def save(self):
        _crud = self.crud()
        try:
            if not self.pk:
                raise DoesNotExist
            _crud.retrieve(self.pk)
        except DoesNotExist:
            response = _crud.create(**self.dict())
        else:
            response = _crud.update(self.pk, **self.dict())
        # TODO: FIXME
        self.__dict__ = response.__dict__

    def delete(self):
        self.crud().delete(self.pk)
