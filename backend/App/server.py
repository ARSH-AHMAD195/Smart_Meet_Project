from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.core.config import setting
from contextlib import asynccontextmanager
from App.core.database import create_db_and_tables
from App.routes import auth, users, teams, meetings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    create_db_and_tables()
    yield

app = FastAPI(title=setting.get_project_name(),
              description=setting.get_project_description(),
              version=setting.get_project_version(),
              lifespan=lifespan)

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/", tags=["MeetUp Root"])
def home():
    return {
        "app": "MeetUp",
        "version": "v0.1.0",
        "message": "MeetUp Landing Page go to /docs for SwaggerUI"
    }

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(meetings.router, prefix="/meets", tags=["Meets"])