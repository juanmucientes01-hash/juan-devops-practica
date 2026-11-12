from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import List

from models import (
    UsuarioCreate, UsuarioRead,
    ProductoCreate, ProductoRead,
    PedidoCreate, PedidoRead
)
from services import TiendaService

app = FastAPI(
    title="API Tienda Online",
    description="Endpoints para gestionar Usuarios, Productos y Pedidos",
    version="1.0.0"
)

# Instancia del servicio en memoria
servicio = TiendaService()

# REDIRECCIÓN DIRECTA A /docs AL ENTRAR A LA RAÍZ (/)
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# ENDPOINTS USUARIOS
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    return servicio.crear_usuario(usuario)

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int):
    u = servicio.obtener_usuario(usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    return servicio.listar_usuarios()

# ENDPOINTS PRODUCTOS
@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    return servicio.crear_producto(producto)

@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    return servicio.listar_productos()

@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int):
    p = servicio.obtener_producto(producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int):
    if not servicio.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")

# ENDPOINTS PEDIDOS
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCreate):
    try:
        return servicio.crear_pedido(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: int):
    if not servicio.obtener_usuario(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return servicio.listar_pedidos_cliente(cliente_id)