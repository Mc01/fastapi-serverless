from typing import List, Optional

from faunadb import query
from faunadb.client import FaunaClient
from faunadb.errors import NotFound
from faunadb.objects import FaunaTime
from pydantic import BaseModel

from app import settings
from .exceptions import DoesNotExist
from .utils import FaunaHelper, now, from_fauna_time


class Crud(FaunaHelper):
    def __init__(self, collection_name: str, model):
        """
        Each CRUD requires that:
        - Fauna client is connected to db
        - collection_name is created / exists
        - Collection is created / exists
        """
        self.collection_name = collection_name
        self.model = model
        self.client = FaunaClient(secret=settings.FAUNADB_SECRET)
        if not self.client.query(
            query.exists(
                query.database(
                    db_name=settings.FAUNADB_DBNAME,
                )
            )
        ):
            self.database = self.client.query(
                query.create_database(db_params={
                    'name': settings.FAUNADB_DBNAME,
                }),
            )
        if not self.client.query(
            query.exists(
                query.collection(
                    collection_name=collection_name,
                )
            )
        ):
            self.collection = self.client.query(
                query.create_collection(collection_params={
                    'name': collection_name,
                }),
            )

    @staticmethod
    def _parse_pk(object_data: dict) -> int:
        """
        Returns parsed id from response
        :param object_data: dict - FaunaDB response
        :return: pk: int - object id
        """
        return int(object_data['ref'].id())

    def _parse_model_instance(self, object_data: dict) -> BaseModel:
        """
        Returns parsed Model from response
        :param object_data: dict - FaunaDB object response
        :return: model: Model - actual Pydantic Model
        """
        object_data['data'] = {
            k: from_fauna_time(v) if isinstance(v, FaunaTime) else v
            for k, v in object_data['data'].items()
        }
        return self.model(
            pk=object_data['ref'].id(),
            **object_data['data'],
        )

    def create(self, **kwargs: dict) -> BaseModel:
        """
        Creates object from supplied kwargs
        :param kwargs: dict - supplied values for new object
        :return: pk: int - FaunaDB created object id
        """
        _now = now()
        kwargs.update(dict(
            created_at=_now,
            updated_at=_now,
        ))
        self.model(
            **kwargs,
        )
        object_data: dict = self.client.query(
            query.create(
                collection_ref=self._expr_collection(),
                params={
                    'data': kwargs,
                },
            ),
        )
        return self._parse_model_instance(
            object_data=object_data,
        )

    def list(self, limit: int = 10) -> List[BaseModel]:
        """
        Returns list of objects
        :param limit: int - limit for pagination
        :return: objects: List[Model]
        """
        object_list: dict = self.client.query(
            query.map_(
                lambda ref: query.get(ref),
                self._expr_documents(limit=limit)
            )
        )
        return [
            self._parse_model_instance(object_data=object_data)
            for object_data in object_list['data']
        ]

    def retrieve(self, pk: int) -> Optional[BaseModel]:
        """
        Returns object from FaunaDB
        :param pk: int - FaunaDB object id
        :return: object: Model
        """
        try:
            object_data: dict = self.client.query(
                query.get(
                    self._expr_reference(pk),
                ),
            )
        except NotFound:
            raise DoesNotExist

        return self._parse_model_instance(
            object_data=object_data,
        )

    def update(self, pk: int, **kwargs: dict) -> BaseModel:
        """
        Updates object in FaunaDB
        :param pk: int - FaunaDB object id
        :param kwargs: dict - supplied values for update
        :return: success: bool
        """
        kwargs.update(dict(
            updated_at=now(),
        ))
        self.model(**kwargs)
        try:
            object_data: dict = self.client.query(
                query.update(
                    self._expr_reference(pk), {
                        'data': kwargs,
                    },
                ),
            )
        except NotFound:
            raise DoesNotExist

        return self._parse_model_instance(
            object_data=object_data,
        )

    def delete(self, pk: int) -> bool:
        """
        Deletes object in FaunaDB
        :param pk: int - FaunaDB object id
        :return: success: bool
        """
        try:
            object_data: dict = self.client.query(
                query.delete(
                    self._expr_reference(pk),
                )
            )
        except NotFound:
            raise DoesNotExist

        return self._parse_pk(object_data) == pk
