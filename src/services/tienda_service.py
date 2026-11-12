from datetime import datetime
from models.usuario import UsuarioCreate, UsuarioRead
from models.producto import ProductoCreate, ProductoRead
from models.pedido import PedidoCreate, PedidoRead, PedidoItemRead

class TiendaService:
    def __init__(self):
        # Bases de datos en memoria 
        self.usuarios = {}
        self.productos = {}
        self.pedidos = {}
        
        # Autoincrementales de IDs
        self._next_u_id = 1
        self._next_p_id = 1
        self._next_ped_id = 1

    # USUARIOS 
    def crear_usuario(self, datos: UsuarioCreate) -> UsuarioRead:
        es_admin = datos.tipo.lower() == "administrador"
        u = UsuarioRead(
            id=self._next_u_id,
            nombre=datos.nombre,
            email=datos.email,
            es_admin=es_admin
        )
        self.usuarios[u.id] = u
        self._next_u_id += 1
        return u

    def obtener_usuario(self, usuario_id: int):
        return self.usuarios.get(usuario_id)

    def listar_usuarios(self):
        return list(self.usuarios.values())

    # PRODUCTOS
    def crear_producto(self, datos: ProductoCreate) -> ProductoRead:
        p = ProductoRead(
            id=self._next_p_id,
            **datos.model_dump()
        )
        self.productos[p.id] = p
        self._next_p_id += 1
        return p

    def obtener_producto(self, producto_id: int):
        return self.productos.get(producto_id)

    def listar_productos(self):
        return list(self.productos.values())

    def eliminar_producto(self, producto_id: int) -> bool:
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False

    #  PEDIDOS 
    def crear_pedido(self, datos: PedidoCreate) -> PedidoRead:
        # Verificar que el cliente existe
        if datos.cliente_id not in self.usuarios:
            raise ValueError("El cliente no existe.")

        items_detallados = []
        total_pedido = 0.0

        for item in datos.items:
            prod = self.obtener_producto(item.producto_id)
            if not prod:
                raise ValueError(f"El producto con ID {item.producto_id} no existe.")
            if prod.stock < item.cantidad:
                raise ValueError(f"Stock insuficiente para '{prod.nombre}'.")
            
            # Descontar stock
            prod.stock -= item.cantidad
            subtotal = prod.precio * item.cantidad
            total_pedido += subtotal

            items_detallados.append(PedidoItemRead(
                producto_id=prod.id,
                nombre_producto=prod.nombre,
                cantidad=item.cantidad,
                precio_unitario=prod.precio
            ))

        pedido = PedidoRead(
            id=self._next_ped_id,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cliente_id=datos.cliente_id,
            total=total_pedido,
            items=items_detallados
        )
        self.pedidos[pedido.id] = pedido
        self._next_ped_id += 1
        return pedido

    def listar_pedidos_cliente(self, cliente_id: int):
        return [p for p in self.pedidos.values() if p.cliente_id == cliente_id]