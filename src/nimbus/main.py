from fastapi import FastAPI

from nimbus.views import base

app = FastAPI()


app.include_router(base)
