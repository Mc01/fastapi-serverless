from common.router import AppRouter
from users.models import User


router = AppRouter()
router.register_model(User)
