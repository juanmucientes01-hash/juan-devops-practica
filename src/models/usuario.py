from pydantic import BaseModel, EmailStr

# Esquema para recibir los datos al registrar un usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    tipo: str  # "cliente" o "administrador"
    direccion_postal: str

# Esquema para devolver la información de un usuario
class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: str
    es_admin: bool