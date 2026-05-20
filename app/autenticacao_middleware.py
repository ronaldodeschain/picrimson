from fastapi import Request 
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import base64
from dotenv import load_dotenv
import os
from app.dependencies import get_database
from app.repositories.usuario import UsuarioRepository

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


class SessionUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        request.state.is_admin = False
        user_id = request.session.get("user_id")
        if user_id is not None:
            try:
                db = get_database()
                usuario_repo = UsuarioRepository(db)
                usuario = await usuario_repo.get_cliente(user_id)
                if usuario:
                    request.state.user = usuario
                    request.state.is_admin = usuario.role == "admin"
            except Exception:
                request.state.user = None
                request.state.is_admin = False
        return await call_next(request)