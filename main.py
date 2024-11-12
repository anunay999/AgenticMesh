from fastapi import FastAPI
from registry_service.main import router as registry_router
from discovery.main import router as discovery_router
from genai_service.main import router as genai_router
from orchestrator_service.main import router as orchestrator_router


app = FastAPI()

# Include routers from registry_service and discovery
app.include_router(registry_router, prefix="/registry")
app.include_router(discovery_router, prefix="/discovery")
app.include_router(genai_router, prefix="/genai")
app.include_router(orchestrator_router, prefix="/orchestrator")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)