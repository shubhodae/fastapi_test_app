from fastapi import FastAPI
import logging

from .settings import AppSettings
environement = AppSettings().ENVIRONMENT


# App configs
app_configs = dict()
app_configs["title"] = "Test App API"

# Show documentation only in 'local' and 'staging'
SHOW_DOCS_ENVIRONMENT = ("local", "staging")
if environement not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None

app = FastAPI(**app_configs)


# Logger
logging.basicConfig(
    level=logging.DEBUG,
    format=' %(name)s :: %(levelname)-8s :: %(message)s'
)


# Routes
from users.views import router as users_router
from items.views import router as items_router
app.include_router(users_router)
app.include_router(items_router)



@app.get("/")
async def root():
    return {
        "message": "Test App API"
    }
