from fastapi import APIRouter, Depends

from app.endpoints.auth.routers import router as auth_router
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

_admin = [Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]

admin_router = APIRouter(prefix="/admin", dependencies=_admin)
# admin_router.include_router(...)  # add admin routers here

base_v1_router = APIRouter()
base_v1_router.include_router(auth_router)
base_v1_router.include_router(admin_router)