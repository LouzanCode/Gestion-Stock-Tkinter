from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
  
  db = 'database/productos.db'
  
  def __init__(self, root):
    self.ventana = root
    self.ventana.title("App Gestor de Produtos") # Titulo de la ventana
    self.ventana.resizable(1,1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
    self.ventana.wm_iconbitmap('recursos/icon.ico')

    # Estilo personalizado para la tabla
    style = ttk.Style()
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11)) # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold')) # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})]) # Eliminamos los bordes

  # Estructura de la tabla
    self.tabla = ttk.Treeview(height = 20, columns = ("#0", "#1", "#2", "#3") , style="mystyle.Treeview")
    self.tabla.grid(row = 4, column = 0, columnspan = 2)
    self.tabla.heading('#0', text = 'Nombre', anchor = CENTER) # Encabezado 0
    self.tabla.heading('#1', text='Precio', anchor = CENTER) # Encabezado 1
    self.tabla.heading('#2', text='Categoría', anchor = CENTER) # Encabezado 1
    self.tabla.heading('#3', text='Stock', anchor = CENTER) # Encabezado 1
   
   # Creacion del menu    
    self.menu = Menu(self.ventana)
    self.ventana.config(menu=self.menu)
    self.productos = Menu(self.menu)
    self.menu.add_cascade(label= "Archivo", menu=self.productos, font=('Calibri', 13))
    self.productos.add_command(label= "Registrar Producto", command=self.registrar_producto)


    
  
    # Botones de Eliminar y Editar
    s = ttk.Style()
    s.configure('my.TButton', font=('Calibri', 14, 'bold'))
    boton_eliminar = ttk.Button(text = 'ELIMINAR', command = self.del_producto,
    style='my.TButton')
    boton_eliminar.grid(row = 5, column = 0, sticky = W + E)
    boton_editar = ttk.Button(text='EDITAR', command = self.edit_producto,
    style='my.TButton')
    boton_editar.grid(row = 5, column = 1, sticky = W + E)


    # Mensaje informativo para el usuario
    self.mensaje = Label(text = '', fg = 'red')
    self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
    
    self.get_productos()
   

  def db_consulta(self, consulta, parametros = ()):
    with sqlite3.connect(self.db) as con: # Iniciamos una conexion con la base de datos (alias con)
      cursor = con.cursor() # Generamos un cursor de la conexion para poder operar en la base de datos
      resultado = cursor.execute(consulta, parametros) # Preparar la consulta SQL (con parametros si los hay)
      con.commit() # Ejecutar la consulta SQL preparada anteriormente
    return resultado # Retornar el resultado de la consulta SQL
    
    
    
  def get_productos(self):
 # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
   registros_tabla = self.tabla.get_children() # Obtener todos los datos de latabla
   for fila in registros_tabla:
    self.tabla.delete(fila)
    # Consulta SQL
   query = 'SELECT * FROM producto ORDER BY nombre DESC'
   registros_db = self.db_consulta(query) # Se hace la llamada al metodo db_consultas
 # Escribir los datos en pantalla
   for fila in registros_db:
     print(fila) # print para verificar por consola los datos
     self.tabla.insert('', 0, text = fila[1], values = (fila[2], fila[3], fila[4]))
     
     
  def validacion_nombre(self):
    
    nombre_introducido_por_usuario = self.nombre
    return len(nombre_introducido_por_usuario) != 0
  
  def validacion_precio(self):
    precio_introducido_por_usuario = self.precio
    return len(precio_introducido_por_usuario) != 0
  
  def registrar_producto(self):
    self.ventana_aniadir = Toplevel() # Crear una ventana por delante de la principal
    self.ventana_aniadir.title = "Registrar Producto" # Titulo de la ventana
    self.ventana_aniadir.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
    self.ventana_aniadir.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana

# Creacion del contenedor Frame de la ventana de Añadir Producto
    frame_ap = LabelFrame(self.ventana_aniadir, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold')) #frame_ap: Frame Añadir Producto
    frame_ap.grid(row = 0, column = 1, columnspan = 2, pady = 20)
  
 # Label Nombre
    self.etiqueta_nombre = Label(frame_ap, text="Nombre: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
    self.etiqueta_nombre.grid(row=1, column=0) # Posicionamiento a traves de grid
  # Entry Nombre (caja de texto que recibira el nombre)
    self.nombre = Entry(frame_ap, font=('Calibri', 13)) # Caja de texto (input de texto) ubicada en el frame
    self.nombre.focus() # Para que el foco del raton vaya a este Entry al inicio
    self.nombre.grid(row=1, column=1)
  # Label Precio
    self.etiqueta_precio = Label(frame_ap, text="Precio: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
    self.etiqueta_precio.grid(row=2, column=0)

  # Entry Precio (caja de texto que recibira el precio)
    self.precio = Entry(frame_ap, font=('Calibri', 13)) # Caja de texto (input de texto) ubicada en el frame
    self.precio.grid(row=2, column=1)
  # Label Categoría
    self.etiqueta_categoria = Label(frame_ap, text="Categoría: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
    self.etiqueta_categoria.grid(row=3, column=0)

  # Entry Categoria (caja de texto que recibira el precio)
    self.categoria = Entry(frame_ap, font=('Calibri', 13)) # Caja de texto (input de texto) ubicada en el frame
    self.categoria.grid(row=3, column=1)

    # Label Stock
    self.etiqueta_stock = Label(frame_ap, text="Stock: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
    self.etiqueta_stock.grid(row=4, column=0)

  # Entry Stock (caja de texto que recibira el precio)
    self.stock = Entry(frame_ap, font=('Calibri', 13)) # Caja de texto (input de texto) ubicada en el frame
    self.stock.grid(row=4, column=1)
    
    s = ttk.Style()
    s.configure('my.TButton', font=('Calibri', 14, 'bold'))
    self.boton_aniadir = ttk.Button(frame_ap, text="Guardar Producto",
    command=self.add_producto, style='my.TButton')
    self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

    self.nombre.delete(0, END) # Borrar el campo nombre del formulario
    self.precio.delete(0, END) # Borrar el campo precio del formulario
    self.categoria.delete(0, END)
    self.stock.delete(0, END)

  def add_producto(self, nombre, precio, categoria, stock):
    self.nombre = nombre
    self.precio = precio
    self.categoria = categoria
    self.stock = stock
    if self.validacion_nombre() and self.validacion_precio():
      query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)' # Consulta SQL (sin los datos)
      parametros = (self.nombre, self.precio, self.categoria, self.stock) # Parametros de la consulta SQL 
      self.db_consulta(query, parametros)
      print("Datos guardados")
      self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre) # Label ubicado entre el boton y la tabla
  
      # Para debug
      #print(self.nombre.get())
      #print(self.precio.get())
    elif self.validacion_nombre() and self.validacion_precio() == False:
      print("El precio es obligatorio")
      self.mensaje['text'] = 'El precio es obligatorio'
    elif self.validacion_nombre() == False and self.validacion_precio():
      print("El nombre es obligatorio")
      self.mensaje['text'] = 'El nombre es obligatorio'
    else:
      print("El nombre y el precio son obligatorios")
      self.mensaje['text'] = 'El nombre y el precio son obligatorios'

    self.get_productos() # 
    self.ventana_aniadir.destroy() # Cerrar la ventana de registro de productos

      
  def del_producto(self):
    # Debug
    #print(self.tabla.item(self.tabla.selection()))
    #print(self.tabla.item(self.tabla.selection())['text'])
    #print(self.tabla.item(self.tabla.selection())['values'])
    #print(self.tabla.item(self.tabla.selection())['values'][0])
    self.mensaje['text'] = '' # Mensaje inicialmente vacio
    # Comprobacion de que se seleccione un producto para poder eliminarlo
    try:
     self.tabla.item(self.tabla.selection())['text'][0]
    except IndexError as e:
     self.mensaje['text'] = 'Por favor, seleccione un producto'
     return
    self.mensaje['text'] = ''
    nombre = self.tabla.item(self.tabla.selection())['text']
    query = 'DELETE FROM producto WHERE nombre = ?' # Consulta SQL
    self.db_consulta(query, (nombre,)) # Ejecutar la consulta
    self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
    self.get_productos() # Actualizar la tabla de productos

  def edit_producto(self):
    self.mensaje['text'] = '' # Mensaje inicialmente vacio
    try:
     self.tabla.item(self.tabla.selection())['text'][0]
    except IndexError as e:
     self.mensaje['text'] = 'Por favor, seleccione un producto'
     return
    nombre = self.tabla.item(self.tabla.selection())['text']
    old_precio = self.tabla.item(self.tabla.selection())['values'][0] # El preciose encuentra dentro de una lista
    self.ventana_editar = Toplevel() # Crear una ventana por delante de la principal
    self.ventana_editar.title = "Editar Producto" # Titulo de la ventana
    self.ventana_editar.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
    self.ventana_editar.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana
   
    
    # Creacion del contenedor Frame de la ventana de Editar Producto
    frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold')) #frame_ep: Frame Editar Producto
    frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
    # Label Nombre antiguo
    self.etiqueta_nombre_anituguo = Label(frame_ep, text = "Nombre antiguo: ",font=('Calibri', 13)) #Etiqueta de texto ubicada en el frame
    self.etiqueta_nombre_anituguo.grid(row=2, column=0) # Posicionamiento a traves de grid
    # Entry Nombre antiguo (texto que no se podra modificar)
    self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13))
    self.input_nombre_antiguo.grid(row=2, column=1)
    # Label Nombre nuevo
    self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
    self.etiqueta_nombre_nuevo.grid(row=3, column=0)
    # Entry Nombre nuevo (texto que si se podra modificar)
    self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
    self.input_nombre_nuevo.grid(row=3, column=1)
    self.input_nombre_nuevo.focus() # Para que el foco del raton vaya a este Entry al inicio
    # Label Precio antiguo
    self.etiqueta_precio_anituguo = Label(frame_ep,text="Precio antiguo: ", font=('Calibri', 13)) #Etiqueta de texto ubicada en el frame
    self.etiqueta_precio_anituguo.grid(row=4, column=0) # Posicionamiento a travesde grid
    # Entry Precio antiguo (texto que no se podra modificar)
    self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly', font=('Calibri', 13))
    self.input_precio_antiguo.grid(row=4, column=1)

  # Label Precio nuevo
    self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
    self.etiqueta_precio_nuevo.grid(row=5, column=0)
    # Entry Precio nuevo (texto que si se podra modificar)
    self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
    self.input_precio_nuevo.grid(row=5, column=1)
    # Boton Actualizar Producto
    s = ttk.Style()
    s.configure('my.TButton', font=('Calibri', 14, 'bold'))
    self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
    style='my.TButton',
    command=lambda:
    self.actualizar_productos(self.input_nombre_nuevo.get(),

    self.input_nombre_antiguo.get(),

    self.input_precio_nuevo.get(),

    self.input_precio_antiguo.get()))
    self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)
 

  def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio,antiguo_precio):
    producto_modificado = False
    query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
    if nuevo_nombre != '' and nuevo_precio != '':
      # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
      parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
      producto_modificado = True
    elif nuevo_nombre != '' and nuevo_precio == '':
 # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
      parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
      producto_modificado = True
    elif nuevo_nombre == '' and nuevo_precio != '':
 # Si el usuario deja vacio el nuevo nombre, se mantiene el nombr anterior
      parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
      producto_modificado = True
    
    if(producto_modificado):

      self.db_consulta(query, parametros) # Ejecutar la consulta
      self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
      self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
      self.get_productos() # Actualizar la tabla de productos
    else:
      self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
      self.mensaje['text'] = 'El producto {} NO ha sidoctualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario

if __name__ == '__main__':
 root = Tk() # Instancia de la ventana principal
 app = Producto(root) # Se envia a la clase Producto el control sobre la ventana root
 root.mainloop() # Comenzamos el bucle de aplicacion, es como un while True
 