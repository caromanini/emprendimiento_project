# CAMI: Cuidado Adulto Mayor Interactivo

## Setup
Se requiere tener PostgreSQL instalado local.

1. Clonar el repositorio.

2. Crear entorno virtual:
```
py -3 -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```
venv\Scripts\activate
```

- Mac/Linux:
```
source venv\bin\activate
```

4. Instalar dependencias:
```
pip install -r requirements.txt
```

5. Configurar la base de datos:

Se requiere PostgreSQL instalado de manera local, yo estoy usando la versión `17.0`

- Crear base de datos en PostgreSQL
- Crear archivo `.env` con lo siguiente:

```
DATABASE_URL=postgresql://postgres:contraseña@localhost:5432/nombre_base_de_datos
```

6. Ejecutar la aplicación:
```
fastapi dev
```
