# from fastapi import FastAPI

# app = FastAPI(
#     title="CyberSentinel API",
#     description="CyberSentinel Backend API Service",
#     version="1.0.0"
# )

# @app.get("/")
# async def root():
#     return {"message": "backend running", "status": "ok"}

# @app.get("/health")
# async def health_check():
#     return {"message": "CyberSentinel API is running", "status": "ok"}



#######################################################################3# chnages 1

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# # Import API Routers
# from app.api.auth import router as auth_router
# from app.api.predictions import router as predictions_router
# from app.api.locations import router as locations_router
# from app.api.alerts import router as alerts_router
# from app.api.dashboard import router as dashboard_router

# app = FastAPI(
#     title="CyberSentinel API",
#     description="Backend API for SIH Problem Statement 2 — Threat Risk Prediction & GIS Heatmap",
#     version="1.0.0"
# )

# # CORS Middleware Setup (Allows React Frontend to connect smoothly)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust to specific React ports (e.g. http://localhost:3000) for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Register API Routers under /api/v1 prefix
# API_PREFIX = "/api/v1"
# app.include_router(auth_router, prefix=API_PREFIX)
# app.include_router(predictions_router, prefix=API_PREFIX)
# app.include_router(locations_router, prefix=API_PREFIX)
# app.include_router(alerts_router, prefix=API_PREFIX)
# app.include_router(dashboard_router, prefix=API_PREFIX)

# @app.get("/", tags=["Health"])
# def root_health_check():
#     return {
#         "system": "CyberSentinel Backend",
#         "status": "online",
#         "message": "All mock API routes active"
#     }



######################################################## changes 2


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.api.auth import router as auth_router
from app.api.predictions import router as predictions_router
from app.api.locations import router as locations_router
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB Atlas
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()

app = FastAPI(
    title="CyberSentinel API",
    description="Backend API for SIH — Threat Risk Prediction & GIS Heatmap",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(predictions_router, prefix=API_PREFIX)
app.include_router(locations_router, prefix=API_PREFIX)
app.include_router(alerts_router, prefix=API_PREFIX)
app.include_router(dashboard_router, prefix=API_PREFIX)

@app.get("/", tags=["Health"])
def root_health_check():
    return {
        "system": "CyberSentinel Backend",
        "status": "online",
        "message": "API with MongoDB Atlas connected"
    }