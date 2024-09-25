import logging
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import APIUsage, User
from app.auth import get_current_user

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define rate limits for each customer (number of requests allowed in the time window)
RATE_LIMITS = {
    "customer1": {"limit": 5, "window": 60},  # 5 requests per 60 seconds (1 minute)
    "customer2": {"limit": 10, "window": 30},  # 10 requests per 30 seconds
    "customer3": {"limit": None, "window": None}  # No rate limiting
}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define paths to exclude from rate limiting
        excluded_paths = excluded_paths = ["/", "/docs", "/redoc", "/openapi.json", "/auth/register", "/auth/login"]

        # Check if the request path is in the excluded list
        if any(request.url.path.startswith(path) for path in excluded_paths):
            return await call_next(request)
        
        db: Session = next(get_db())

        # Extract user information using dependency injection
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header is None or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="User not authenticated")
            
            token = auth_header.split(" ")[1]
            current_user = await get_current_user(token=token, db=db)
        except HTTPException as e:
            return Response(content=str(e.detail), status_code=e.status_code)
        except Exception:
            return Response(content="User not authenticated", status_code=401)

        # Check the user's role for rate-limiting purposes
        customer_type = current_user.role.lower()

        # Proceed with rate limiting logic as before
        if customer_type not in RATE_LIMITS or RATE_LIMITS[customer_type]["limit"] is None:
            # No rate limiting for this customer
            return await call_next(request)

        # Get rate limit details
        rate_limit = RATE_LIMITS[customer_type]["limit"]
        window = RATE_LIMITS[customer_type]["window"]

        # Check the number of API calls made by this user in the given window
        window_start_time = datetime.utcnow() - timedelta(seconds=window)
        api_call_count = (
            db.query(APIUsage)
            .filter(
                APIUsage.user_id == current_user.id,
                APIUsage.endpoint == str(request.url.path),
                APIUsage.timestamp >= window_start_time
            )
            .count()
        )

        if api_call_count >= rate_limit:
            # Properly handle 429 Too Many Requests
            return Response(content="Rate limit exceeded. Please try again later.", status_code=429)

        # Log the API usage
        api_usage = APIUsage(user_id=current_user.id, endpoint=str(request.url.path))
        db.add(api_usage)
        db.commit()

        # Proceed with the request
        response = await call_next(request)
        return response