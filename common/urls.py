from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from common.crud import Crud
from common.exceptions import DoesNotExist


class Urls(APIRouter):
    crud: Crud

    def __init__(self, crud: Crud, **kwargs):
        self.crud: Crud = crud
        super(Urls, self).__init__(**kwargs)
        self._bind_urls()

    def _bind_urls(self):
        # create
        self.add_api_route(
            path='',
            endpoint=self.get_create(),
            status_code=status.HTTP_201_CREATED,
            methods=['POST'],
            response_model=self.crud.model,
        )
        # read
        self.add_api_route(
            path='',
            endpoint=self.get_list(),
            status_code=status.HTTP_200_OK,
            methods=['GET'],
            response_model=List[self.crud.model],
        )
        # retrieve
        self.add_api_route(
            path='/{pk}',
            endpoint=self.get_retrieve(),
            status_code=status.HTTP_200_OK,
            methods=['GET'],
            response_model=self.crud.model,
        )
        # update
        self.add_api_route(
            path='/{pk}',
            endpoint=self.get_update(),
            status_code=status.HTTP_200_OK,
            methods=['PATCH'],
            response_model=self.crud.model,
        )
        # delete
        self.add_api_route(
            path='/{pk}',
            endpoint=self.get_delete(),
            status_code=status.HTTP_204_NO_CONTENT,
            methods=['DELETE'],
        )

    def get_create(self):
        _model: BaseModel = self.crud.model

        async def _create(model: _model) -> _model:
            return self.crud.create(**model.dict())

        return _create

    def get_list(self):
        _model = self.crud.model

        async def _list() -> List[_model]:
            return self.crud.list()

        return _list

    def get_retrieve(self):
        _model = self.crud.model

        async def _retrieve(pk: int) -> _model:
            try:
                return self.crud.retrieve(pk)
            except DoesNotExist:
                raise HTTPException(status_code=404, detail='Item not found')

        return _retrieve

    def get_update(self):
        _model: BaseModel = self.crud.model

        async def _update(pk: int, model: _model) -> _model:
            try:
                model_dict = model.dict(exclude_unset=True)
                return self.crud.update(pk, **model_dict)
            except DoesNotExist:
                raise HTTPException(status_code=404, detail='Item not found')

        return _update

    def get_delete(self):
        _model: BaseModel = self.crud.model

        async def _delete(pk: int):
            try:
                assert self.crud.delete(pk)
            except DoesNotExist:
                raise HTTPException(status_code=404, detail='Item not found')

        return _delete
