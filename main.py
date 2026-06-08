from fastapi import FastAPI
from app.routers import router
from app.utils.lifespan import on_startup
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(debug=True, lifespan=on_startup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)