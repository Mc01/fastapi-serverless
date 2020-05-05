from mangum import Mangum

from app.main import api


handler = Mangum(api)
