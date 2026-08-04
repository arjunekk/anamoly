"""
Entry point for the FastAPI backend.
Handles application startup (loading the PatchCore model once),
static file serving (for heatmap images), and route registration.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import MODEL_PATH, HEATMAP_DIR
from app.api.model_state import load_patchcore_model
from app.api.inspection_routes import router as inspection_router
from app.api.history_routes import router as history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: loading PatchCore model...")
    load_patchcore_model(str(MODEL_PATH))
    yield
    print("Shutting down.")


app = FastAPI(title="Industrial Defect Detection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static/heatmaps", StaticFiles(directory=str(HEATMAP_DIR)), name="heatmaps")

app.include_router(inspection_router)
app.include_router(history_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}