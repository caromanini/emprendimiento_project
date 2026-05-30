# CAMI: Cuidado Adulto Mayor Interactivo

## Setup
Se requiere tener PostgreSQL instalado local.

1. Clonar el repositorio.

2. Crear entorno virtual:

- Mac/Linux:
```
python3 -m venv venv
```

- Windows:
```
py -3 -m venv venv
```

3. Activar el entorno virtual:

- Mac/Linux:
```
source venv/bin/activate
```

- Windows:
```
venv\Scripts\activate
```

4. Instalar dependencias:
```
pip install -r requirements.txt
```

5. Configurar la base de datos:

Se requiere PostgreSQL instalado de manera local, versión `17.0` recomendada.

- Crear la base de datos en PostgreSQL:
```
psql -d postgres -c "CREATE DATABASE cami_project;"
```

- Copiar el archivo de ejemplo y completar los valores:
```
cp .env.example .env
```

El archivo `.env` debe quedar así (ajustá los valores a tu entorno):

```
DATABASE_URL=postgresql://<tu_usuario_del_sistema>@localhost:5432/cami_project
SECRET_KEY=tu_secret_key_aqui
GEMINI_API_KEY=tu_gemini_api_key_aqui
COOKIE_SECURE=false
```
6. Ejecutar la aplicación:
```
fastapi dev
```
