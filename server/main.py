from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api import api_v1_router
from server.agents.web_search import ensure_initialised

load_dotenv()

# -- Server lifespan --
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # -- Startup --
    # Setup MCP client
    try:
        await ensure_initialised()
    except Exception as e:
        print(f"[WARN] MCP preload failed: {e}")

    yield
    # -- Shutdown --

# -- Setup server --
app = FastAPI(
    title='Agentic AI Server Template',
    docs_url='/',
    lifespan=lifespan
)

# -- CORS middleware --
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# -- API routers --
app.include_router(api_v1_router, prefix='/api/v1')



