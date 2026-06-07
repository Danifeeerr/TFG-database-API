# TFG API

> **Language / Idioma:** [English](README.md) | Español

API REST desarrollada como parte del Trabajo de Fin de Grado. Proporciona acceso y gestión de la base de datos del sistema, siendo el backend compartido por las otras dos aplicaciones del proyecto.

## Proyectos del TFG

Este repositorio es uno de los tres componentes que forman el TFG:

| Proyecto | Descripción | Repositorio |
|---|---|---|
| **API** (este repo) | Backend REST, gestión de la base de datos | — |
| **Aplicación de escritorio** | Cliente de administración | [Ver repositorio](https://github.com/Danifeeerr/VRdashboard-TFG) |
| **Aplicación de Realidad Virtual** | Aplicación principal de entrenamiento | [Ver repositorio](https://github.com/Danifeeerr/occupational-safety-TFG) |

---

## Stack tecnológico

- **Python** + **FastAPI**
- **PostgreSQL** con **SQLAlchemy**
- **Pydantic v2** para validación de esquemas
- **JWT** para autenticación
- **Argon2** para hashing de contraseñas

## Requisitos previos

- Python 3.10+
- PostgreSQL en ejecución y accesible

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd TFGAPI

# Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
dburl=postgresql://usuario:contraseña@host:puerto/nombre_bd
skey=tu_clave_secreta_jwt
```

## Ejecución

```bash
uvicorn main:app --reload
```

La API quedará disponible en `http://localhost:8000`.
La documentación interactiva (Swagger UI) se genera automáticamente en `http://localhost:8000/docs`.

---

## Endpoints

### Autenticación

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/login` | Inicia sesión y devuelve un token JWT |

### Usuarios

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/users` | Lista todos los usuarios |
| `GET` | `/user` | Obtiene el usuario a partir de un token |
| `GET` | `/user/{id}` | Obtiene un usuario por ID *(solo admin)* |
| `POST` | `/users/new` | Crea un nuevo usuario |
| `POST` | `/users/update` | Actualiza los datos de un usuario |
| `DELETE` | `/users/delete/{id}` | Elimina un usuario *(solo admin)* |

### Entrenamientos

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/training` | Lista todos los entrenamientos |
| `GET` | `/training/{id}` | Obtiene un entrenamiento por ID |
| `POST` | `/training/new` | Crea un nuevo entrenamiento |
| `POST` | `/training/update` | Actualiza un entrenamiento |
| `DELETE` | `/training/delete/{id}` | Elimina un entrenamiento |

### Asignaciones

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/assignation` | Lista todas las asignaciones |
| `GET` | `/assignation/{userid}` | Lista las asignaciones de un usuario *(solo admin)* |
| `POST` | `/assignation/new` | Crea una asignación usuario–entrenamiento *(solo admin)* |
| `POST` | `/assignation/update` | Marca una asignación como completada |
| `DELETE` | `/assignation/delete` | Elimina una asignación *(solo admin)* |

### Intentos

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/attempt` | Obtiene los intentos de un usuario en un entrenamiento |
| `GET` | `/attempt/user` | Obtiene todos los intentos de un usuario |
| `GET` | `/attempt/timestamp` | Obtiene un intento por usuario y timestamp |
| `POST` | `/attempt/new` | Registra un nuevo intento |
| `DELETE` | `/attempt/delete` | Elimina un intento |

---

## Modelos de datos

```
users           training        assignation         attempt
─────────────   ────────────    ───────────────     ───────────────
id              id              userid (FK)         userid (FK)
username        name            trainingid (FK)     trainingid (FK)
password_hash   hours           completed           time_spent
admin           error_limit     date                number_errors
                                                    timestamp
```
