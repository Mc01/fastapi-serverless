from common.models import Model


class User(Model):
    class Meta:
        collection: str = 'users'
        url: str = 'users'

    username: str
    email: str
