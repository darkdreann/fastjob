from typing import Annotated
from fastapi import APIRouter, Depends, status, Query, Path
from api.security.permissions import PermissionsManager
from api.models.enums import CandidateField

candidateRoute = APIRouter(prefix="/candidates", tags=["candidates"])
