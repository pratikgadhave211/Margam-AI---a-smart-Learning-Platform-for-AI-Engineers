import urllib.request
import json
from fastapi import APIRouter, Request, HTTPException, Security
from fastapi.security import APIKeyCookie

router = APIRouter()

# Better Auth sets this cookie automatically on login
cookie_sec = APIKeyCookie(name="better-auth.session_token", auto_error=False)

def verify_token(request: Request, token: str = Security(cookie_sec)):
    # 1. Check if token exists
    if not token:
        # Fallback to check if it's running under HTTPS locally (__Secure- prefix)
        token = request.cookies.get("__Secure-better-auth.session_token")
        
    if not token:
        raise HTTPException(status_code=401, detail="Authentication token missing")
        
    try:
        # 2. Verify the session by calling the Better Auth endpoint
        req = urllib.request.Request("http://localhost:3000/api/auth/get-session")
        # Forward the exact cookies from the client
        req.add_header("cookie", request.headers.get("cookie", ""))
        
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise HTTPException(status_code=401, detail="Invalid session")
            data = json.loads(response.read().decode())
            if not data or "session" not in data:
                raise HTTPException(status_code=401, detail="Invalid session data")
            return data["user"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
