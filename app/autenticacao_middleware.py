from fastapi import Request 
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import base64
from dotenv import load_dotenv
import os

load_dotenv()



USERNAME = os.getenv("DOCS_USERNAME")
PASSWORD = os.getenv("DOCS_PASSWORD")

class DocsAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request, call_next):
        path = request.url.path
        
        #rotas protegidas
        if path.startswith("/docs") or path.startswith("/redoc") or path.startswith("/openapi.json"):
            auth = request.headers.get("Authorization")
            
            if not auth:
                return self._unauthorized()
            
            try:
                scheme, credentials = auth.split()
                if scheme.lower() != "basic":
                    return self._unauthorized()
                
                decoded = base64.b64decode(credentials).decode("utf-8")
                username, password = decoded.split(":", 1)
                
                if username != USERNAME or password != PASSWORD:
                    return self._unauthorized()
            except Exception:
                return self._unauthorized()
        return await call_next(request)
        
    def _unauthorized(self):
        return Response(
            status_code=401,
            headers={"WWW-Authenticate":"Basic"},
            content="You shall not pass!",
        )