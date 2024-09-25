from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, auth
from app.middleware import LoggingMiddleware
from app.limiter import RateLimitMiddleware  # Ensure to import the correct limiter

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the rate limiting middleware first
app.add_middleware(RateLimitMiddleware)

# Add the logging middleware
app.add_middleware(LoggingMiddleware)

# Include the auth and user routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1")
