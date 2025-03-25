from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post
from .routers import user
from .routers import auth
from .routers import vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine) # No longer needed because of integration of alembic migration tool

app = FastAPI()

# domains allowed to be talked to
# origins = ["https://www.google.com"]

# allowing all domains to access api
origins = ["*"]


# Allowing Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():

    return {"Greet": "Welcome to API Development using FastAPI"}
