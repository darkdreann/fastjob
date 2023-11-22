from typing import Annotated
from fastapi import APIRouter, Depends, status, Query, Path
from api.security.permissions import PermissionsManager

candidateRoute = APIRouter(prefix="/candidates", tags=["candidates"])
candidateRoute2 = APIRouter(prefix=candidateRoute.prefix, tags=candidateRoute.tags)