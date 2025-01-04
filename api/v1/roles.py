"""
Roles v1
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.authentications import get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError
from models.permiso import Permiso
from models.rol import Rol
from schemas.rol import OneRolOut
from schemas.usuario import UsuarioInDB

roles = APIRouter(prefix="/api/v1/roles", tags=["sistema"])


def get_rol(database: Session, rol_id: int) -> Rol:
    """Consultar un rol por su ID"""
    rol = database.query(Rol).get(rol_id)
    if rol is None:
        raise MyNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese rol, está eliminado")
    return rol


@roles.get("/{rol_id}", response_model=OneRolOut)
async def detalle_rol(
    current_user: Annotated[UsuarioInDB, Depends(get_current_user)],
    database: Annotated[Session, Depends(get_db)],
    rol_id: int,
):
    """Detalle de un rol a partir de su ID"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        rol = get_rol(database, rol_id)
    except MyAnyError as error:
        return OneRolOut(success=False, message=str(error))
    return OneRolOut.model_validate(rol)
