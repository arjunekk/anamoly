"""
Entry point for the FastAPI backend.

Handles application startup (loading the PatchCore model once),
static file serving (for heatmap images), and route registration.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import MODEL_PATH, HEATMAP_DIR
from app.api.model_state import load_patchcore_model
from app.api.inspection_routes import router as inspection_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once when the server starts (before the 'yield') and once
    when it shuts down (after the 'yield'). We use this to load the
    PatchCore model exactly one time, rather than per-request.
    """
    print("Starting up: loading PatchCore model...")
    load_patchcore_model(str(MODEL_PATH))
    yield
    print("Shutting down.")


app = FastAPI(title="Industrial Defect Detection API", lifespan=lifespan)

# Serve heatmap images as static files, accessible at /static/heatmaps/<filename>
app.mount("/static/heatmaps", StaticFiles(directory=str(HEATMAP_DIR)), name="heatmaps")

# Register the inspection route(s).
app.include_router(inspection_router)


@app.get("/health")
def health_check():
    """Basic endpoint to confirm the server is running."""
    return {"status": "ok"}