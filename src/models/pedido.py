from pydantic import BaseModel
from typing import List

# Representa un producto y su cantidad durante la creación
class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int

# Esquema para crear un pedido
class PedidoCreate(BaseModel):
    cliente_id: int
    items: List[PedidoItemCreate]

# Estructura de salida para cada elemento en la lista del pedido
class PedidoItemRead(BaseModel):
    producto_id: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float

# Estructura completa de respuesta de un pedido
class PedidoRead(BaseModel):
    id: int
    fecha: str
    cliente_id: int
    total: float
    items: List[PedidoItemRead]