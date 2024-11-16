from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Coinche server", version="0.1.0")


# CORS to allow the client to access the API from another origin (other domain, other port, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Root"], summary="Health endpoint")
def health():
    return {"message": "Healthy!"}
