"""
ArtesanApp - Sistema de Gestión de Inventario para Artesanías
==============================================================

Este módulo implementa una aplicación de escritorio para la gestión de inventario
de productos artesanales, utilizando SQLite como base de datos y Tkinter para
la interfaz gráfica.

Autor: Jhon Sebastian Gutierrez Garnica
Materia: Programación Avanzada
Ficha: 54477
Versión: 1.0
Fecha: 2025
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Nombre del archivo de base de datos SQLite
DB_FILENAME = "artesanapp.db"

# ------------------ BASE DE DATOS ------------------

def init_db():
    """
    Inicializa la base de datos y crea la tabla de productos si no existe.
    
    Crea una conexión a la base de datos SQLite y ejecuta el script SQL
    para crear la tabla 'productos' con todos sus campos necesarios.
    
    Campos de la tabla:
        - id: Identificador único autoincrementable
        - nombre: Nombre del producto (obligatorio)
        - categoria: Categoría del producto (obligatorio)
        - precio: Precio en pesos colombianos (obligatorio)
        - stock: Cantidad disponible en inventario (obligatorio)
        - disponible: Estado de disponibilidad (1=Sí, 0=No)
        - proveedor: Nombre del proveedor (opcional)
        - tipo_envio: Tipo de envío (Local, Nacional, Internacional)
    
    Returns:
        None
    """
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            disponible INTEGER NOT NULL,
            proveedor TEXT,
            tipo_envio TEXT
        )
    """)
    conn.commit()
    conn.close()

def insertar_producto(data):
    """
    Inserta un nuevo producto en la base de datos.
    
    Args:
        data (tuple): Tupla con los datos del producto en el siguiente orden:
                     (nombre, categoria, precio, stock, disponible, proveedor, tipo_envio)
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    
    Ejemplo:
        >>> data = ("Collar artesanal", "Joyería", 45000.0, 10, 1, "Artesanos Unidos", "Nacional")
        >>> insertar_producto(data)
        True
    """
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock, disponible, proveedor, tipo_envio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error al insertar:", e)
        return False

def consultar_todos():
    """
    Consulta todos los productos registrados en la base de datos.
    
    Returns:
        list: Lista de tuplas, donde cada tupla representa un producto con todos sus campos.
              Formato: [(id, nombre, categoria, precio, stock, disponible, proveedor, tipo_envio), ...]
    
    Ejemplo:
        >>> productos = consultar_todos()
        >>> print(productos[0])
        (1, 'Collar artesanal', 'Joyería', 45000.0, 10, 1, 'Artesanos Unidos', 'Nacional')
    """
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute("SELECT id, nombre, categoria, precio, stock, disponible, proveedor, tipo_envio FROM productos")
    rows = c.fetchall()
    conn.close()
    return rows

def eliminar_producto(producto_id):
    """
    Elimina un producto de la base de datos según su ID.
    
    Args:
        producto_id (int): ID único del producto a eliminar.
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    
    Ejemplo:
        >>> eliminar_producto(5)
        True
    """
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error al eliminar:", e)
        return False

# ------------------ GUI ------------------

class ArtesanApp(tk.Tk):
    """
    Clase principal de la aplicación ArtesanApp.
    
    Esta clase hereda de tk.Tk y representa la ventana principal de la aplicación.
    Gestiona la interfaz gráfica completa incluyendo formularios, tabla de productos
    y todas las funcionalidades de CRUD (Crear, Leer, Actualizar, Eliminar).
    
    Attributes:
        nombre_var (StringVar): Variable para el nombre del producto
        categoria_var (StringVar): Variable para la categoría del producto
        precio_var (StringVar): Variable para el precio del producto
        stock_var (StringVar): Variable para el stock del producto
        disponible_var (IntVar): Variable para la disponibilidad (1=Sí, 0=No)
        proveedor_var (StringVar): Variable para el proveedor del producto
        tipo_envio_var (StringVar): Variable para el tipo de envío
        search_var (StringVar): Variable para el campo de búsqueda
        tree (Treeview): Componente tabla para mostrar los productos
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal y todos sus componentes.
        
        Configura:
            - Título y dimensiones de la ventana
            - Header con el logo de la aplicación
            - Formulario de registro de productos
            - Panel de búsqueda y acciones
            - Tabla de visualización de productos
        """
        super().__init__()
        self.title("ArtesanApp - Gestión de Inventario")
        self.geometry("950x600")
        self.configure(bg="#f7f7f7")

        # ---------- HEADER ----------
        # Crea la barra superior con el título de la aplicación
        header = tk.Frame(self, bg="#2b6cb0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🧺 ArtesanApp", fg="white", bg="#2b6cb0", 
                font=("Helvetica", 20, "bold")).pack(side="left", padx=16)

        # ---------- CONTENIDO PRINCIPAL ----------
        # Contenedor principal para el formulario y la tabla
        content = tk.Frame(self, bg="#f7f7f7", padx=12, pady=12)
        content.pack(fill="both", expand=True)

        # ---------- FORMULARIO IZQUIERDO ----------
        # Panel de registro de productos con todos los campos necesarios
        form_frame = tk.LabelFrame(content, text="Registrar Producto", padx=12, pady=12, 
                                  bg="white", font=("Helvetica", 10, "bold"))
        form_frame.pack(side="left", fill="y", padx=(0,12))

        style = {"font": ("Helvetica", 10), "bg": "white"}

        # Campo: Nombre del producto
        tk.Label(form_frame, text="Nombre:", **style).grid(row=0, column=0, sticky="w")
        self.nombre_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=4)

        # Campo: Categoría (lista desplegable)
        tk.Label(form_frame, text="Categoría:", **style).grid(row=1, column=0, sticky="w")
        self.categoria_var = tk.StringVar()
        categorias = ["Decoración", "Joyería", "Textil", "Papelería", "Otros"]
        ttk.Combobox(form_frame, textvariable=self.categoria_var, values=categorias, 
                    state="readonly", width=28).grid(row=1, column=1, pady=4)

        # Campo: Precio en pesos colombianos
        tk.Label(form_frame, text="Precio (COP):", **style).grid(row=2, column=0, sticky="w")
        self.precio_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.precio_var, width=30).grid(row=2, column=1, pady=4)

        # Campo: Stock disponible
        tk.Label(form_frame, text="Stock:", **style).grid(row=3, column=0, sticky="w")
        self.stock_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.stock_var, width=30).grid(row=3, column=1, pady=4)

        # Campo: Checkbox de disponibilidad
        self.disponible_var = tk.IntVar(value=1)
        tk.Checkbutton(form_frame, text="Disponible (a la venta)", variable=self.disponible_var, 
                      bg="white").grid(row=4, column=1, sticky="w", pady=4)

        # Campo: Proveedor
        tk.Label(form_frame, text="Proveedor:", **style).grid(row=5, column=0, sticky="w")
        self.proveedor_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.proveedor_var, width=30).grid(row=5, column=1, pady=4)

        # Campo: Tipo de envío (botones de radio)
        tk.Label(form_frame, text="Tipo envío:", **style).grid(row=6, column=0, sticky="w")
        self.tipo_envio_var = tk.StringVar(value="Local")
        rb_frame = tk.Frame(form_frame, bg="white")
        rb_frame.grid(row=6, column=1, sticky="w")
        for tipo in ["Local", "Nacional", "Internacional"]:
            tk.Radiobutton(rb_frame, text=tipo, variable=self.tipo_envio_var, 
                          value=tipo, bg="white").pack(side="left", padx=2)

        # Botones de acción del formulario
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="💾 Guardar", command=self.on_guardar, 
                 bg="#2b6cb0", fg="white", width=12).pack(side="left", padx=6)
        tk.Button(btn_frame, text="🧹 Limpiar", command=self.limpiar_form, 
                 bg="#e2e8f0", width=10).pack(side="left", padx=6)

        # ---------- PANEL DERECHO ----------
        # Contiene la búsqueda y la tabla de productos
        right_frame = tk.Frame(content, bg="#f7f7f7")
        right_frame.pack(side="right", fill="both", expand=True)

        # Barra de búsqueda y botones de acción
        search_frame = tk.Frame(right_frame, bg="#f7f7f7")
        search_frame.pack(fill="x", pady=(0,10))
        tk.Label(search_frame, text="Buscar por nombre:", bg="#f7f7f7").pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=6)
        tk.Button(search_frame, text="🔍 Buscar", command=self.on_buscar, 
                 bg="#2b6cb0", fg="white").pack(side="left", padx=4)
        tk.Button(search_frame, text="📋 Mostrar todo", command=self.mostrar_todos, 
                 bg="#e2e8f0").pack(side="left", padx=4)
        tk.Button(search_frame, text="🗑 Eliminar seleccionado", command=self.on_eliminar, 
                 bg="#e53e3e", fg="white").pack(side="right", padx=6)

        # ---------- TABLA ----------
        # Tabla para visualizar todos los productos
        columns = ("id", "nombre", "categoria", "precio", "stock", "disponible", "proveedor", "tipo_envio")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        
        # Configuración de columnas con anchos personalizados
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            if col == "nombre":
                self.tree.column(col, width=180)
            elif col == "proveedor":
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        # Cargar todos los productos al iniciar
        self.mostrar_todos()

    # ---------- EVENTOS ----------

    def on_guardar(self):
        """
        Maneja el evento de guardar un nuevo producto.
        
        Valida los datos del formulario, convierte los tipos de datos necesarios
        y llama a la función insertar_producto(). Muestra mensajes de éxito o error.
        
        Validaciones:
            - Campos obligatorios no vacíos
            - Precio debe ser un número válido
            - Stock debe ser un entero válido
        
        Returns:
            None
        """
        # Obtener valores del formulario
        nombre = self.nombre_var.get().strip()
        categoria = self.categoria_var.get().strip()
        precio = self.precio_var.get().strip()
        stock = self.stock_var.get().strip()
        disponible = 1 if self.disponible_var.get() else 0
        proveedor = self.proveedor_var.get().strip()
        tipo_envio = self.tipo_envio_var.get()

        # Validar campos obligatorios
        if not nombre or not categoria or not precio or not stock:
            messagebox.showwarning("Validación", "Por favor complete los campos obligatorios.")
            return
        
        # Validar tipos de datos numéricos
        try:
            precio_f = float(precio)
            stock_i = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser número y stock entero.")
            return

        # Insertar producto en la base de datos
        data = (nombre, categoria, precio_f, stock_i, disponible, proveedor, tipo_envio)
        if insertar_producto(data):
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.limpiar_form()
            self.mostrar_todos()

    def limpiar_form(self):
        """
        Limpia todos los campos del formulario y los resetea a sus valores por defecto.
        
        Valores por defecto:
            - Campos de texto: vacíos
            - Disponible: Sí (1)
            - Tipo de envío: Local
        
        Returns:
            None
        """
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")
        self.disponible_var.set(1)
        self.proveedor_var.set("")
        self.tipo_envio_var.set("Local")

    def mostrar_todos(self):
        """
        Actualiza la tabla mostrando todos los productos de la base de datos.
        
        Limpia la tabla actual y la vuelve a llenar con todos los registros.
        Formatea el precio con dos decimales y convierte el campo disponible
        a texto legible ("Sí" o "No").
        
        Returns:
            None
        """
        # Limpiar tabla actual
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Cargar todos los productos
        for row in consultar_todos():
            disponible_text = "Sí" if row[5] == 1 else "No"
            self.tree.insert("", "end", values=(row[0], row[1], row[2], f"{row[3]:.2f}", 
                                               row[4], disponible_text, row[6], row[7]))

    def on_buscar(self):
        """
        Filtra los productos en la tabla según el texto de búsqueda.
        
        Busca coincidencias en el nombre del producto (búsqueda insensible a mayúsculas).
        Actualiza la tabla mostrando solo los productos que coinciden con la búsqueda.
        
        Returns:
            None
        """
        q = self.search_var.get().strip().lower()
        
        # Limpiar tabla
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Filtrar y mostrar resultados
        for row in consultar_todos():
            if q in row[1].lower():
                disponible_text = "Sí" if row[5] == 1 else "No"
                self.tree.insert("", "end", values=(row[0], row[1], row[2], f"{row[3]:.2f}", 
                                                   row[4], disponible_text, row[6], row[7]))

    def on_eliminar(self):
        """
        Elimina el producto seleccionado en la tabla.
        
        Solicita confirmación al usuario antes de eliminar. Si se confirma,
        elimina el producto de la base de datos y actualiza la tabla.
        
        Muestra advertencias si:
            - No hay ningún producto seleccionado
            - Ocurre un error durante la eliminación
        
        Returns:
            None
        """
        # Verificar que haya un producto seleccionado
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return
        
        # Obtener datos del producto seleccionado
        item = self.tree.item(selected[0])
        producto_id = item["values"][0]
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar", 
                                     f"¿Desea eliminar el producto '{item['values'][1]}'?")
        if confirm:
            if eliminar_producto(producto_id):
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                self.mostrar_todos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")


# ------------------ MAIN ------------------
if __name__ == "__main__":
    """
    Punto de entrada de la aplicación.
    
    Inicializa la base de datos y lanza la interfaz gráfica.
    """
    init_db()
    app = ArtesanApp()
    app.mainloop()