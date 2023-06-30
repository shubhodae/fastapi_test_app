from fastapi import FastAPI
import logging

app = FastAPI()


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
        "message": "Hello World"
    }
