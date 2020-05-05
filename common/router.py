from fastapi import APIRouter


class AppRouter(APIRouter):
    def register_model(self, model):
        urls_router = model.urls()
        prefix = f'/{model.Meta.url}'
        super(AppRouter, self).include_router(
            router=urls_router,
            prefix=prefix,
        )
