from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import Base, engine
from routers import auth, booking, appoinment

app = FastAPI()

# ✅ Add CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # CRA default
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://docter-frontend.vercel.app/",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],          # allow all headers
)

Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(booking.router)
app.include_router(appoinment.router)


@app.get("/")
def home():
    return {"Message": "All Good"}
