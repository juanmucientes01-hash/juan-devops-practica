# juan-devops-practica

**Autor:** Juan Mucientes Prieto

## Descripción

API REST de una **tienda online** hecha con **Python y FastAPI** (Práctica 2).
Permite gestionar **usuarios**, **productos** y **pedidos**. Los datos se guardan en memoria.

Estructura del código (`src/`):

```
src/
├── main.py                 # Endpoints de la API
├── models/                 # Esquemas Pydantic (usuario, producto, pedido)
└── services/
    └── tienda_service.py   # Lógica de negocio
```

## Ejecutar sin Docker

```bash
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

## Docker

### Construir la imagen

```bash
docker build -t tienda-api:1.0 .
```

### Ejecutar el contenedor

```bash
docker run -p 8000:8000 tienda-api:1.0
```

En segundo plano:

```bash
docker run -d --name tienda-api -p 8000:8000 tienda-api:1.0
```

### Variables de entorno

| Variable | Por defecto | Descripción |
|----------|-------------|-------------|
| `PORT`   | `8000`      | Puerto en el que escucha la API |

Ejemplo cambiando el puerto:

```bash
docker run -p 9000:9000 -e PORT=9000 tienda-api:1.0
```

### Salida esperada y pruebas

Al arrancar, `docker logs tienda-api` muestra:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Abre **http://localhost:8000/docs** para ver y probar todos los endpoints (Swagger).

| Método | Endpoint                       | Qué hace |
|--------|--------------------------------|----------|
| POST   | `/usuarios`                    | Crea un usuario |
| GET    | `/usuarios`                    | Lista usuarios |
| GET    | `/usuarios/{id}`               | Obtiene un usuario |
| POST   | `/productos`                   | Crea un producto |
| GET    | `/productos`                   | Lista productos |
| GET    | `/productos/{id}`              | Obtiene un producto |
| DELETE | `/productos/{id}`              | Elimina un producto |
| POST   | `/pedidos`                     | Crea un pedido (descuenta stock) |
| GET    | `/usuarios/{id}/pedidos`       | Pedidos de un cliente |

Ejemplos con `curl`:

```bash
curl -X POST http://localhost:8000/usuarios -H "Content-Type: application/json" \
  -d '{"nombre":"Ana","email":"ana@example.com","tipo":"cliente","direccion_postal":"Calle 1"}'

curl -X POST http://localhost:8000/productos -H "Content-Type: application/json" \
  -d '{"nombre":"Camiseta","precio":15.5,"stock":10,"tipo":"ropa","talla":"M"}'

curl -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" \
  -d '{"cliente_id":1,"items":[{"producto_id":1,"cantidad":2}]}'
# {"id":1,"fecha":"...","cliente_id":1,"total":31.0,"items":[...]}
```

### Subir la imagen a Docker Hub (push)

```bash
docker login
docker tag tienda-api:1.0 juanmucip/tienda-api:1.0
docker push juanmucip/tienda-api:1.0
```

### Descargar la imagen (pull)

```bash
docker pull juanmucip/tienda-api:1.0
docker run -p 8000:8000 juanmucip/tienda-api:1.0
```

Imagen publicada: https://hub.docker.com/r/juanmucip/tienda-api
