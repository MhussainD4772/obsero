from fastapi import FastAPI

# uvicorn will load this as app.main:app
app = FastAPI(title="Obsero API")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
