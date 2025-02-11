import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

# Clases para la gestión de datos
class Cliente:
    def __init__(self, id_cliente, nombre, direccion, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class Venta:
    def __init__(self, id_venta, cliente, productos):
        self.id_venta = id_venta
        self.cliente = cliente
        self.productos = productos  # Lista de diccionarios con 'id_producto', 'producto', 'cantidad', 'precio'
        self.subtotal = sum(p['cantidad'] * p['precio'] for p in productos)
        self.iva = self.subtotal * 0.16
        self.total = self.subtotal + self.iva

# Datos en memoria
clientes_db = {}
productos_db = {}
ventas_db = {}

# Aplicación principal
class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda - Sistema de Gestión")
        self.root.geometry("900x700")
        self.style = ttk.Style(theme='flatly')  # Aplicar tema moderno

        # Configurar Notebook para organizar las pestañas
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Variables para la venta actual
        self.current_sale_products = []
        self.selected_sale_product_index = None  # Para rastrear el producto seleccionado

        # Crear pestañas para cada módulo
        self.create_client_tab()
        self.create_product_tab()
        self.create_new_sale_tab()
        self.create_sales_tab()

    # Pestaña de Clientes
    def create_client_tab(self):
        self.client_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.client_frame, text="Clientes")

        # Frame para los campos de entrada
        input_frame = ttk.Frame(self.client_frame, padding=10)
        input_frame.pack(fill=X)

        ttk.Label(input_frame, text="ID Cliente:").grid(row=0, column=0, sticky=W, pady=5)
        self.client_id_entry = ttk.Entry(input_frame)
        self.client_id_entry.grid(row=0, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Nombre:").grid(row=1, column=0, sticky=W, pady=5)
        self.client_name_entry = ttk.Entry(input_frame)
        self.client_name_entry.grid(row=1, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Dirección:").grid(row=2, column=0, sticky=W, pady=5)
        self.client_address_entry = ttk.Entry(input_frame)
        self.client_address_entry.grid(row=2, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Teléfono:").grid(row=3, column=0, sticky=W, pady=5)
        self.client_phone_entry = ttk.Entry(input_frame)
        self.client_phone_entry.grid(row=3, column=1, pady=5, sticky=EW)

        # Asegurar que las columnas se expandan correctamente
        input_frame.columnconfigure(1, weight=1)

        # Frame para los botones
        button_frame = ttk.Frame(self.client_frame, padding=10)
        button_frame.pack(fill=X)

        ttk.Button(button_frame, text="Agregar Cliente", command=self.add_client, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Editar Cliente", command=self.edit_client, bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar Cliente", command=self.delete_client, bootstyle="danger").pack(side=LEFT, padx=5)

        # Tabla para mostrar los clientes
        table_frame = ttk.Frame(self.client_frame, padding=10)
        table_frame.pack(fill=BOTH, expand=True)

        self.client_table = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Dirección", "Teléfono"), show='headings')
        self.client_table.heading("ID", text="ID Cliente")
        self.client_table.heading("Nombre", text="Nombre")
        self.client_table.heading("Dirección", text="Dirección")
        self.client_table.heading("Teléfono", text="Teléfono")
        self.client_table.pack(fill=BOTH, expand=True)
        self.client_table.bind("<Double-1>", self.load_client_data)

    def add_client(self):
        id_cliente = self.client_id_entry.get()
        nombre = self.client_name_entry.get()
        direccion = self.client_address_entry.get()
        telefono = self.client_phone_entry.get()

        if id_cliente and nombre and direccion and telefono:
            cliente = Cliente(id_cliente, nombre, direccion, telefono)
            clientes_db[id_cliente] = cliente
            self.update_client_table()
            self.clear_client_fields()
            Messagebox.show_info(f"Cliente {nombre} agregado.", "Éxito")
        else:
            Messagebox.show_error("Todos los campos son obligatorios.", "Error")

    def delete_client(self):
        selected = self.client_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un cliente para eliminar.", "Error")
            return

        id_cliente = self.client_table.item(selected[0], 'values')[0]
        del clientes_db[id_cliente]
        self.update_client_table()
        Messagebox.show_info("Cliente eliminado correctamente.", "Éxito")

    def load_client_data(self, event):
        selected = self.client_table.focus()
        values = self.client_table.item(selected, "values")

        if values:
            self.client_id_entry.delete(0, ttk.END)
            self.client_id_entry.insert(0, values[0])
            self.client_name_entry.delete(0, ttk.END)
            self.client_name_entry.insert(0, values[1])
            self.client_address_entry.delete(0, ttk.END)
            self.client_address_entry.insert(0, values[2])
            self.client_phone_entry.delete(0, ttk.END)
            self.client_phone_entry.insert(0, values[3])

    def edit_client(self):
        id_cliente = self.client_id_entry.get()
        nombre = self.client_name_entry.get()
        direccion = self.client_address_entry.get()
        telefono = self.client_phone_entry.get()

        if id_cliente in clientes_db:
            cliente = clientes_db[id_cliente]
            cliente.nombre = nombre
            cliente.direccion = direccion
            cliente.telefono = telefono
            self.update_client_table()
            self.clear_client_fields()
            Messagebox.show_info("Cliente actualizado correctamente.", "Éxito")
        else:
            Messagebox.show_error("Cliente no encontrado.", "Error")

    def clear_client_fields(self):
        self.client_id_entry.delete(0, ttk.END)
        self.client_name_entry.delete(0, ttk.END)
        self.client_address_entry.delete(0, ttk.END)
        self.client_phone_entry.delete(0, ttk.END)

    def update_client_table(self):
        for row in self.client_table.get_children():
            self.client_table.delete(row)
        for cliente in clientes_db.values():
            self.client_table.insert("", ttk.END, values=(cliente.id_cliente, cliente.nombre, cliente.direccion, cliente.telefono))

    # Pestaña de Productos
    def create_product_tab(self):
        self.product_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.product_frame, text="Productos")

        # Frame para los campos de entrada
        input_frame = ttk.Frame(self.product_frame, padding=10)
        input_frame.pack(fill=X)

        ttk.Label(input_frame, text="ID Producto:").grid(row=0, column=0, sticky=W, pady=5)
        self.product_id_entry = ttk.Entry(input_frame)
        self.product_id_entry.grid(row=0, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Nombre:").grid(row=1, column=0, sticky=W, pady=5)
        self.product_name_entry = ttk.Entry(input_frame)
        self.product_name_entry.grid(row=1, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Precio:").grid(row=2, column=0, sticky=W, pady=5)
        self.product_price_entry = ttk.Entry(input_frame)
        self.product_price_entry.grid(row=2, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Stock:").grid(row=3, column=0, sticky=W, pady=5)
        self.product_stock_entry = ttk.Entry(input_frame)
        self.product_stock_entry.grid(row=3, column=1, pady=5, sticky=EW)

        # Asegurar que las columnas se expandan correctamente
        input_frame.columnconfigure(1, weight=1)

        # Frame para los botones
        button_frame = ttk.Frame(self.product_frame, padding=10)
        button_frame.pack(fill=X)

        ttk.Button(button_frame, text="Agregar Producto", command=self.add_product, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Editar Producto", command=self.edit_product, bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar Producto", command=self.delete_product, bootstyle="danger").pack(side=LEFT, padx=5)

        # Tabla para mostrar los productos
        table_frame = ttk.Frame(self.product_frame, padding=10)
        table_frame.pack(fill=BOTH, expand=True)

        self.product_table = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Precio", "Stock"), show='headings')
        self.product_table.heading("ID", text="ID Producto")
        self.product_table.heading("Nombre", text="Nombre")
        self.product_table.heading("Precio", text="Precio")
        self.product_table.heading("Stock", text="Stock")
        self.product_table.pack(fill=BOTH, expand=True)
        self.product_table.bind("<Double-1>", self.load_product_data)

    def add_product(self):
        id_producto = self.product_id_entry.get()
        nombre = self.product_name_entry.get()
        try:
            precio = float(self.product_price_entry.get())
            stock = int(self.product_stock_entry.get())
        except ValueError:
            Messagebox.show_error("Precio debe ser un número y Stock debe ser un entero.", "Error")
            return

        if id_producto and nombre and precio >= 0 and stock >= 0:
            producto = Producto(id_producto, nombre, precio, stock)
            productos_db[id_producto] = producto
            self.update_product_table()
            self.clear_product_fields()
            Messagebox.show_info(f"Producto {nombre} agregado.", "Éxito")
        else:
            Messagebox.show_error("Todos los campos son obligatorios y deben ser valores válidos.", "Error")

    def delete_product(self):
        selected = self.product_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un producto para eliminar.", "Error")
            return

        id_producto = self.product_table.item(selected[0], 'values')[0]
        del productos_db[id_producto]
        self.update_product_table()
        Messagebox.show_info("Producto eliminado correctamente.", "Éxito")

    def load_product_data(self, event):
        selected = self.product_table.focus()
        values = self.product_table.item(selected, "values")

        if values:
            self.product_id_entry.delete(0, ttk.END)
            self.product_id_entry.insert(0, values[0])
            self.product_name_entry.delete(0, ttk.END)
            self.product_name_entry.insert(0, values[1])
            self.product_price_entry.delete(0, ttk.END)
            self.product_price_entry.insert(0, values[2])
            self.product_stock_entry.delete(0, ttk.END)
            self.product_stock_entry.insert(0, values[3])

    def edit_product(self):
        id_producto = self.product_id_entry.get()
        nombre = self.product_name_entry.get()
        try:
            precio = float(self.product_price_entry.get())
            stock = int(self.product_stock_entry.get())
        except ValueError:
            Messagebox.show_error("Precio debe ser un número y Stock debe ser un entero.", "Error")
            return

        if id_producto in productos_db:
            producto = productos_db[id_producto]
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            self.update_product_table()
            self.clear_product_fields()
            Messagebox.show_info("Producto actualizado correctamente.", "Éxito")
        else:
            Messagebox.show_error("Producto no encontrado.", "Error")

    def clear_product_fields(self):
        self.product_id_entry.delete(0, ttk.END)
        self.product_name_entry.delete(0, ttk.END)
        self.product_price_entry.delete(0, ttk.END)
        self.product_stock_entry.delete(0, ttk.END)

    def update_product_table(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        for producto in productos_db.values():
            self.product_table.insert("", ttk.END, values=(producto.id_producto, producto.nombre, producto.precio, producto.stock))

    # Nueva Pestaña de Realizar Venta
    def create_new_sale_tab(self):
        self.new_sale_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.new_sale_frame, text="Realizar Venta")

        # Frame para los campos de entrada
        input_frame = ttk.Frame(self.new_sale_frame, padding=10)
        input_frame.pack(fill=X)

        ttk.Label(input_frame, text="ID Cliente:").grid(row=0, column=0, sticky=W, pady=5)
        self.new_sale_client_id_entry = ttk.Entry(input_frame)
        self.new_sale_client_id_entry.grid(row=0, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="ID Producto:").grid(row=1, column=0, sticky=W, pady=5)
        self.new_sale_product_id_entry = ttk.Entry(input_frame)
        self.new_sale_product_id_entry.grid(row=1, column=1, pady=5, sticky=EW)

        ttk.Label(input_frame, text="Cantidad:").grid(row=2, column=0, sticky=W, pady=5)
        self.new_sale_quantity_entry = ttk.Entry(input_frame)
        self.new_sale_quantity_entry.grid(row=2, column=1, pady=5, sticky=EW)

        # Asegurar que las columnas se expandan correctamente
        input_frame.columnconfigure(1, weight=1)

        # Frame para los botones de producto
        product_button_frame = ttk.Frame(self.new_sale_frame, padding=10)
        product_button_frame.pack(fill=X)

        ttk.Button(product_button_frame, text="Agregar Producto", command=self.add_product_to_sale, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(product_button_frame, text="Editar Producto", command=self.edit_product_in_sale, bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Button(product_button_frame, text="Eliminar Producto", command=self.delete_product_from_sale, bootstyle="danger").pack(side=LEFT, padx=5)

        # Tabla para mostrar los productos agregados a la venta
        table_frame = ttk.Frame(self.new_sale_frame, padding=10)
        table_frame.pack(fill=BOTH, expand=True)

        self.sale_products_table = ttk.Treeview(table_frame, columns=("ID Producto", "Nombre", "Cantidad", "Precio", "Importe"), show='headings')
        self.sale_products_table.heading("ID Producto", text="ID Producto")
        self.sale_products_table.heading("Nombre", text="Nombre")
        self.sale_products_table.heading("Cantidad", text="Cantidad")
        self.sale_products_table.heading("Precio", text="Precio")
        self.sale_products_table.heading("Importe", text="Importe")
        self.sale_products_table.pack(fill=BOTH, expand=True)
        self.sale_products_table.bind("<Double-1>", self.load_sale_product_data)

        # Botón para finalizar la venta
        finalize_button_frame = ttk.Frame(self.new_sale_frame, padding=10)
        finalize_button_frame.pack(fill=X)

        ttk.Button(finalize_button_frame, text="Finalizar Venta", command=self.finalize_sale, bootstyle="primary").pack(side=RIGHT, padx=5)

    # ... [Métodos relacionados con la venta se mantienen igual, reemplazando 'messagebox' por 'Messagebox'] ...

    def add_product_to_sale(self):
        id_producto = self.new_sale_product_id_entry.get()
        try:
            cantidad = int(self.new_sale_quantity_entry.get())
        except ValueError:
            Messagebox.show_error("La cantidad debe ser un número entero.", "Error")
            return

        if id_producto in productos_db:
            producto = productos_db[id_producto]
            if cantidad <= producto.stock:
                importe = cantidad * producto.precio
                self.current_sale_products.append({
                    'id_producto': id_producto,
                    'producto': producto.nombre,
                    'cantidad': cantidad,
                    'precio': producto.precio
                })
                self.update_sale_products_table()
                self.new_sale_product_id_entry.delete(0, ttk.END)
                self.new_sale_quantity_entry.delete(0, ttk.END)
                self.selected_sale_product_index = None  # Reiniciar selección
            else:
                Messagebox.show_error(f"Stock insuficiente para el producto {producto.nombre}.", "Error")
        else:
            Messagebox.show_error("Producto no encontrado.", "Error")

    def update_sale_products_table(self):
        for row in self.sale_products_table.get_children():
            self.sale_products_table.delete(row)
        for index, item in enumerate(self.current_sale_products):
            importe = item['cantidad'] * item['precio']
            self.sale_products_table.insert("", ttk.END, iid=index, values=(item['id_producto'], item['producto'], item['cantidad'], f"{item['precio']:.2f}", f"{importe:.2f}"))
        self.selected_sale_product_index = None  # Reiniciar selección

    def load_sale_product_data(self, event):
        selected_iid = self.sale_products_table.focus()
        if selected_iid:
            self.selected_sale_product_index = int(selected_iid)
            item = self.current_sale_products[self.selected_sale_product_index]
            self.new_sale_product_id_entry.delete(0, ttk.END)
            self.new_sale_product_id_entry.insert(0, item['id_producto'])
            self.new_sale_quantity_entry.delete(0, ttk.END)
            self.new_sale_quantity_entry.insert(0, str(item['cantidad']))
        else:
            Messagebox.show_error("No se ha seleccionado un producto.", "Error")

    def edit_product_in_sale(self):
        if self.selected_sale_product_index is not None:
            id_producto = self.new_sale_product_id_entry.get()
            try:
                cantidad = int(self.new_sale_quantity_entry.get())
            except ValueError:
                Messagebox.show_error("La cantidad debe ser un número entero.", "Error")
                return

            if id_producto in productos_db:
                producto = productos_db[id_producto]
                if cantidad <= producto.stock:
                    # Actualizar el producto en current_sale_products
                    self.current_sale_products[self.selected_sale_product_index] = {
                        'id_producto': id_producto,
                        'producto': producto.nombre,
                        'cantidad': cantidad,
                        'precio': producto.precio
                    }
                    self.update_sale_products_table()
                    self.new_sale_product_id_entry.delete(0, ttk.END)
                    self.new_sale_quantity_entry.delete(0, ttk.END)
                    self.selected_sale_product_index = None
                else:
                    Messagebox.show_error(f"Stock insuficiente para el producto {producto.nombre}.", "Error")
            else:
                Messagebox.show_error("Producto no encontrado.", "Error")
        else:
            Messagebox.show_error("No se ha seleccionado un producto para editar.", "Error")

    def delete_product_from_sale(self):
        if self.selected_sale_product_index is not None:
            # Eliminar el producto de current_sale_products
            del self.current_sale_products[self.selected_sale_product_index]
            self.update_sale_products_table()
            self.new_sale_product_id_entry.delete(0, ttk.END)
            self.new_sale_quantity_entry.delete(0, ttk.END)
            self.selected_sale_product_index = None
        else:
            Messagebox.show_error("No se ha seleccionado un producto para eliminar.", "Error")

    def finalize_sale(self):
        id_cliente = self.new_sale_client_id_entry.get()
        if id_cliente not in clientes_db:
            Messagebox.show_error("Cliente no encontrado.", "Error")
            return

        if not self.current_sale_products:
            Messagebox.show_error("No hay productos en la venta.", "Error")
            return

        # Verificar stock para todos los productos
        for item in self.current_sale_products:
            producto = productos_db[item['id_producto']]
            if item['cantidad'] > producto.stock:
                Messagebox.show_error(f"Stock insuficiente para el producto {producto.nombre}.", "Error")
                return

        # Actualizar stock
        for item in self.current_sale_products:
            producto = productos_db[item['id_producto']]
            producto.stock -= item['cantidad']

        # Actualizar tabla de productos
        self.update_product_table()

        # Crear venta
        venta = Venta(len(ventas_db) + 1, clientes_db[id_cliente], self.current_sale_products.copy())
        ventas_db[venta.id_venta] = venta

        # Actualizar tabla de ventas
        self.update_sales_table()

        # Limpiar campos y lista de productos
        self.new_sale_client_id_entry.delete(0, ttk.END)
        self.current_sale_products = []
        self.update_sale_products_table()

        # Mostrar ticket
        self.show_ticket(venta)

        Messagebox.show_info(f"Venta {venta.id_venta} registrada.", "Éxito")

    # Pestaña de Ventas
    def create_sales_tab(self):
        self.sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_frame, text="Ventas")

        # Tabla para mostrar las ventas
        table_frame = ttk.Frame(self.sales_frame, padding=10)
        table_frame.pack(fill=BOTH, expand=True)

        self.sales_table = ttk.Treeview(table_frame, columns=("ID Venta", "Cliente", "Productos", "Total"), show='headings')
        self.sales_table.heading("ID Venta", text="ID Venta")
        self.sales_table.heading("Cliente", text="Cliente")
        self.sales_table.heading("Productos", text="Productos")
        self.sales_table.heading("Total", text="Total")
        self.sales_table.pack(fill=BOTH, expand=True)

        self.update_sales_table()

    def update_sales_table(self):
        for row in self.sales_table.get_children():
            self.sales_table.delete(row)
        for venta in ventas_db.values():
            productos_str = ", ".join(f"{p['producto']} (x{p['cantidad']})" for p in venta.productos)
            self.sales_table.insert("", ttk.END, values=(venta.id_venta, venta.cliente.nombre, productos_str, f"{venta.total:.2f}"))

    def show_ticket(self, venta):
        # Crear una nueva ventana de ticket con estilo
        ticket_window = ttk.Toplevel(self.root)
        ticket_window.title(f"Ticket de Venta - ID {venta.id_venta}")
        ticket_window.geometry("400x400")

        # Frame principal para dar padding al contenido
        main_frame = ttk.Frame(ticket_window, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Sección de información del cliente
        client_info_frame = ttk.Frame(main_frame, padding=10, bootstyle="primary")
        client_info_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(client_info_frame, text="Información del Cliente", bootstyle="inverse").grid(row=0, column=0,
                                                                                               columnspan=2, pady=5)
        ttk.Label(client_info_frame, text="Nombre:", bootstyle="info").grid(row=1, column=0, sticky=W)
        ttk.Label(client_info_frame, text=venta.cliente.nombre).grid(row=1, column=1, sticky=W)

        # Sección de productos
        products_frame = ttk.Frame(main_frame, padding=10, bootstyle="secondary")
        products_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(products_frame, text="Productos", bootstyle="inverse").grid(row=0, column=0, columnspan=2, pady=5)

        row_idx = 1
        for producto in venta.productos:
            importe = producto['cantidad'] * producto['precio']
            detalle = f"{producto['producto']} - Cantidad: {producto['cantidad']} - Precio: {producto['precio']:.2f} - Importe: {importe:.2f}"
            ttk.Label(products_frame, text=detalle).grid(row=row_idx, column=0, sticky=W, pady=2)
            row_idx += 1

        # Sección de totales
        totals_frame = ttk.Frame(main_frame, padding=10, bootstyle="success")
        totals_frame.pack(fill=X)
        ttk.Label(totals_frame, text="Resumen de Pago", bootstyle="inverse").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(totals_frame, text="Subtotal:", bootstyle="info").grid(row=1, column=0, sticky=W)
        ttk.Label(totals_frame, text=f"{venta.subtotal:.2f}").grid(row=1, column=1, sticky=E)
        ttk.Label(totals_frame, text="IVA (16%):", bootstyle="info").grid(row=2, column=0, sticky=W)
        ttk.Label(totals_frame, text=f"{venta.iva:.2f}").grid(row=2, column=1, sticky=E)
        ttk.Label(totals_frame, text="Total:", bootstyle="info").grid(row=3, column=0, sticky=W)
        ttk.Label(totals_frame, text=f"{venta.total:.2f}", bootstyle="inverse").grid(row=3, column=1, sticky=E)

# Ejecutar aplicación
if __name__ == "__main__":
    root = ttk.Window(themename='flatly')  # Crear ventana principal con tema
    app = TiendaApp(root)
    root.mainloop()
