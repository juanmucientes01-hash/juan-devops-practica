from pydantic import BaseModel
from typing import Optional

# Esquema para recibir los datos de entrada al crear un producto
class ProductoCreate(BaseModel):
    tipo: str = "generico"  # "generico", "electronico" o "ropa"
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None  # para electronicos
    talla: Optional[str] = None          #  para ropa
    color: Optional[str] = None          #  para ropa

# Esquema para responder con la información del producto (incluye ID)
class ProductoRead(ProductoCreate):
    id: int