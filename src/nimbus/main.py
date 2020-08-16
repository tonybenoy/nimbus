from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"result":"success","message":"Api is up!"}