from datetime import datetime

from faunadb import query
from faunadb.objects import FaunaTime
from pytz import timezone

from app import settings


class FaunaHelper:
    def _expr_collection(self):
        """
        Returns collection query
        :return: query_collection: Expr - FaunaDB expression for collection
        """
        return query.collection(
            collection_name=self.collection_name,
        )

    def _expr_reference(self, pk: int):
        """
        Returns reference query
        :param pk: int - object reference id
        :return: query_reference: Expr - FaunaDB expression for reference
        """
        return query.ref(
            collection_ref=self._expr_collection(),
            id=str(pk),
        )

    def _expr_documents(self, limit=10):
        """
        Returns documents query
        :param limit: int - limit for pagination
        :return: query_reference: Expr - FaunaDB expression for documents
        """
        return query.paginate(
            set=query.documents(
                self._expr_collection(),
            ),
            size=limit,
        )


def now() -> datetime:
    tz = timezone(settings.TIMEZONE)
    return datetime.now().astimezone(tz)


def from_fauna_time(fauna_time: FaunaTime) -> datetime:
    tz = timezone(settings.TIMEZONE)
    return fauna_time.to_datetime().astimezone(tz)
