from contextlib import asynccontextmanager
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from app.api.auth import auth_router
from app.api.ref_codes import refs_router
from app.repositories.redis.redis_manager import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    app.state.redis = redis_manager
    yield
    await redis_manager.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(refs_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
