# ArtesanApp - Sistema de Gestión de Inventario

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**ArtesanApp** es una aplicación de escritorio desarrollada en Python para la gestión de inventario de productos artesanales. Permite registrar, consultar, buscar y eliminar productos de manera sencilla mediante una interfaz gráfica intuitiva.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Base de Datos](#base-de-datos)
- [Funcionalidades](#funcionalidades)

## Características

- **Registro de productos**: Guarda información completa de productos artesanales
- **Búsqueda inteligente**: Filtra productos por nombre en tiempo real
- **Visualización en tabla**: Lista ordenada de todos los productos
- **Eliminación segura**: Confirmación antes de eliminar productos
- **Base de datos SQLite**: Almacenamiento persistente y eficiente
- **Interfaz moderna**: Diseño limpio y fácil de usar con Tkinter
- **Categorización**: Organiza productos en diferentes categorías
- **Gestión de envíos**: Controla tipos de envío (Local, Nacional, Internacional)

## Requisitos

### Requisitos del Sistema

- **Sistema Operativo**: Windows, macOS o Linux
- **Python**: Versión 3.7 o superior
- **Espacio en disco**: Mínimo 50 MB

### Dependencias

Las siguientes bibliotecas vienen incluidas con Python:

- `tkinter` - Interfaz gráfica
- `sqlite3` - Base de datos
- `ttk` - Widgets avanzados para Tkinter

**Nota**: En sistemas Linux, puede que necesites instalar tkinter manualmente:
```bash
sudo apt-get install python3-tk
```

## Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
git clone https://github.com/tu-usuario/artesanapp.git
cd artesanapp
```

O descarga el archivo `artesanapp.py` directamente.

### Paso 2: Verificar instalación de Python

```bash
python --version
# o
python3 --version
```

Deberías ver una versión 3.7 o superior.

### Paso 3: Ejecutar la aplicación

```bash
python artesanapp.py
# o
python3 artesanapp.py
```

La aplicación creará automáticamente el archivo de base de datos `artesanapp.db` en el directorio actual.

## Uso

### Inicio Rápido

1. **Ejecuta la aplicación**:
   ```bash
   python artesanapp.py
   ```

2. **Registra un producto**:
   - Completa los campos del formulario en el panel izquierdo
   - Haz clic en el botón "Guardar"

3. **Busca productos**:
   - Escribe el nombre en el campo de búsqueda
   - Haz clic en "Buscar"

4. **Elimina productos**:
   - Selecciona un producto de la tabla
   - Haz clic en "Eliminar seleccionado"
   - Confirma la eliminación

### Campos del Formulario

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| **Nombre** | Texto | Sí | Nombre del producto artesanal |
| **Categoría** | Lista | Sí | Decoración, Joyería, Textil, Papelería, Otros |
| **Precio (COP)** | Número | Sí | Precio en pesos colombianos |
| **Stock** | Entero | Sí | Cantidad disponible en inventario |
| **Disponible** | Checkbox | No | Si está disponible para venta (por defecto: Sí) |
| **Proveedor** | Texto | No | Nombre del proveedor |
| **Tipo envío** | Radio | No | Local, Nacional o Internacional (por defecto: Local) |

## Estructura del Proyecto

```
artesanapp/
│
├── artesanapp.py          # Archivo principal de la aplicación
├── artesanapp.db          # Base de datos SQLite (se crea automáticamente)
└── README.md              # Documentación del proyecto
```

### Estructura del Código

```
artesanapp.py
├── Importaciones
├── Constantes (DB_FILENAME)
│
├── BASE DE DATOS
│   ├── init_db()           # Inicializa la base de datos
│   ├── insertar_producto() # Inserta nuevos productos
│   ├── consultar_todos()   # Consulta todos los productos
│   └── eliminar_producto() # Elimina productos por ID
│
├── GUI (Interfaz Gráfica)
│   └── ArtesanApp (Clase Principal)
│       ├── __init__()      # Inicializa la ventana
│       ├── on_guardar()    # Guarda nuevos productos
│       ├── limpiar_form()  # Limpia el formulario
│       ├── mostrar_todos() # Muestra todos los productos
│       ├── on_buscar()     # Busca productos
│       └── on_eliminar()   # Elimina productos
│
└── MAIN
    └── Punto de entrada de la aplicación
```

## Base de Datos

### Esquema de la Tabla `productos`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL | Nombre del producto |
| `categoria` | TEXT | NOT NULL | Categoría del producto |
| `precio` | REAL | NOT NULL | Precio en COP |
| `stock` | INTEGER | NOT NULL | Cantidad en inventario |
| `disponible` | INTEGER | NOT NULL | Estado (1=Sí, 0=No) |
| `proveedor` | TEXT | NULL | Nombre del proveedor |
| `tipo_envio` | TEXT | NULL | Local/Nacional/Internacional |

### Ejemplo de Consulta SQL

```sql
-- Ver todos los productos disponibles
SELECT * FROM productos WHERE disponible = 1;

-- Productos por categoría
SELECT * FROM productos WHERE categoria = 'Joyería';

-- Productos con stock bajo
SELECT * FROM productos WHERE stock < 5;
```

## Funcionalidades

### 1. Registro de Productos

Permite agregar nuevos productos con validación de datos:
- Verifica campos obligatorios
- Valida tipos de datos (precio numérico, stock entero)
- Muestra mensajes de confirmación

### 2. Consulta de Productos

Visualiza todos los productos en una tabla interactiva:
- Muestra información completa
- Formato de precio con dos decimales
- Estado de disponibilidad en texto legible

### 3. Búsqueda de Productos

Filtra productos por nombre:
- Búsqueda insensible a mayúsculas/minúsculas
- Resultados en tiempo real
- Opción para mostrar todos los productos

### 4. Eliminación de Productos

Elimina productos de forma segura:
- Requiere selección en la tabla
- Solicita confirmación del usuario
- Actualiza la vista automáticamente

### 5. Gestión de Formulario

- Limpieza rápida de campos
- Valores por defecto inteligentes
- Validación antes de guardar


**Desarrollado con Python y Tkinter**

*Última actualización: Noviembre 2025*