# Import necessary libraries
import tkinter as tk  # GUI library
from tkinter import simpledialog, messagebox, Listbox, Toplevel, PhotoImage, filedialog  # Additional GUI components
from cryptography.fernet import Fernet  # For encryption
from PIL import Image, ImageTk  # For image handling
import json  # For JSON data manipulation
import os  # For OS operations like file handling

# Path to the data file
archivo_datos = "biblioteca_usuarios.json"

# Encryption key, should ideally be generated with Fernet.generate_key() and kept secret
clave = b'jksIXEwi3aG1nMSUSLgR-FQsuekDHEYKUWLDSdkk9SU='
fernet = Fernet(clave)  # Create Fernet object for encryption/decryption

class BibliotecaApp:       
    def __init__(self, root):
        # Initial setup
        self.root = root
        self.root.title("Biblioteca Personal")  # Window title
        self.datos = self.cargar_datos()  # Load data

        # Login frame
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(padx=10, pady=10)

        # Username entry
        self.label_usuario = tk.Label(self.frame_login, text="Usuario:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self.frame_login)
        self.entry_usuario.pack()

        # Password entry
        self.label_password = tk.Label(self.frame_login, text="Contraseña:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame_login, show="*")
        self.entry_password.pack()
        # Bind Enter key to login function
        self.entry_password.bind("<Return>", self.login)
        self.entry_usuario.bind("<Return>", self.login)

        # Login button
        self.button_login = tk.Button(self.frame_login, text="Iniciar Sesión", command=self.login)
        self.button_login.pack(pady=5)

        # Registration button
        self.button_registro = tk.Button(self.frame_login, text="Registrar nuevo usuario", command=self.registrar_usuario)
        self.button_registro.pack(pady=5)

    def mostrar_interfaz_principal(self, usuario):
        # Setup main interface after login
        self.usuario_actual = usuario
        # Clear login frame
        for widget in self.frame_login.winfo_children():
            widget.destroy()
        self.frame_login.pack_forget()

        # Main frame setup
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Search functionality
        self.label_buscar = tk.Label(self.frame_principal, text="Buscar:")
        self.label_buscar.pack()
        self.entry_buscar = tk.Entry(self.frame_principal)
        self.entry_buscar.pack()
        # Dynamic search suggestions
        self.entry_buscar.bind('<KeyRelease>', self.actualizar_sugerencias)
        # Handling key presses in search
        self.entry_buscar.bind('<KeyPress>', self.manejar_teclas_en_buscar)

        # Results listbox
        self.listbox_resultados = Listbox(self.frame_principal)
        self.listbox_resultados.pack(expand=True, fill=tk.BOTH)
        # Bindings for selecting search results
        self.listbox_resultados.bind('<Return>', self.mostrar_detalle_consulta_con_enter)
        self.listbox_resultados.bind('<Button-1>', self.mostrar_detalle_consulta_con_click)

        # Buttons for managing consultations
        self.button_añadir_consulta = tk.Button(self.frame_principal, text="Añadir Consulta", command=self.formulario_añadir_consulta)
        self.button_añadir_consulta.pack()
        self.button_editar_consulta = tk.Button(self.frame_principal, text="Editar Consulta", command=self.editar_consulta)
        self.button_editar_consulta.pack()
        self.button_borrar_consulta = tk.Button(self.frame_principal, text="Borrar Consulta", command=self.borrar_consulta)
        self.button_borrar_consulta.pack()

    # Login function
    def login(self, event=None):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_password.get()

        # Check if credentials are correct
        if usuario in self.datos and self.datos[usuario]["contraseña"] == contraseña:
            messagebox.showinfo("Login", "Inicio de sesión exitoso")
            self.mostrar_interfaz_principal(usuario)
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

    # User registration function
    def registrar_usuario(self):
        # Retrieve the username and password from the entry fields
        usuario = self.entry_usuario.get()
        contraseña = self.entry_password.get()

        # Check if both username and password fields are filled
        if usuario and contraseña: 
            # Check if the username already exists in the data
            if usuario in self.datos:
                # If the username exists, show an error message
                messagebox.showerror("Registro", "El usuario ya existe. Por favor, elija un nombre de usuario diferente.")
            else:
                # If the username doesn't exist, create a new user with the entered username and password
                self.datos[usuario] = {"contraseña": contraseña, "datos": {}}
                # Save the updated data to the JSON file
                self.guardar_datos(self.datos)
                # Show a message that the user has been successfully registered
                messagebox.showinfo("Registro", "Usuario registrado exitosamente. Por favor, inicie sesión.")
        else:
            # If either username or password field is empty, show an error message
            messagebox.showerror("Registro", "Por favor, complete ambos campos.")

    # Update suggestions based on the search query
    def actualizar_sugerencias(self, event):
        consulta = self.entry_buscar.get()
        self.listbox_resultados.delete(0, tk.END)  # Clear previous results

        # Display matching titles as suggestions in the listbox
        if consulta:
            for titulo in self.datos[self.usuario_actual]["datos"]:
                if consulta.lower() in titulo.lower():
                    self.listbox_resultados.insert(tk.END, titulo)

    # Show the details of a selected query from the listbox
    def mostrar_detalle_consulta(self, event):
        try:
            widget = event.widget
            index = widget.curselection()[0]
            titulo = widget.get(index)
            contenido = self.datos[self.usuario_actual]["datos"][titulo]

            # Create a new window to display the selected query's details
            detalle_ventana = tk.Toplevel(self.root)
            detalle_ventana.title(titulo)

            # Split the content into text and optional image path
            partes = contenido.split('\n', 1)
            texto = partes[0]
            tk.Label(detalle_ventana, text=texto, wraplength=400).pack()

            # If there's an image path, try to load and display the image
            if len(partes) > 1 and os.path.isfile(partes[1]):
                try:
                    img = Image.open(partes[1])
                    img = img.resize((250, 250), Image.ANTIALIAS)
                    foto = ImageTk.PhotoImage(img)
                    etiqueta_imagen = tk.Label(detalle_ventana, image=foto)
                    etiqueta_imagen.image = foto
                    etiqueta_imagen.pack()
                except Exception as e:
                    print(f"No se pudo cargar la imagen: {e}")
        except IndexError:
            pass  # Do nothing if there's no selection

    # Handle arrow key navigation in search box
    def manejar_teclas_en_buscar(self, event):
        if event.keysym == 'Down':  # When the down arrow key is pressed
            if len(self.listbox_resultados.get(0, tk.END)) > 0:  # If the listbox has items
                self.listbox_resultados.focus_set()  # Focus on the listbox
                self.listbox_resultados.select_set(0)  # Select the first item
                return "break"  # Prevent default behavior

    # Display query details when an item in the listbox is selected with the enter key
    def mostrar_detalle_consulta_con_enter(self, event=None):
        try:
            index = self.listbox_resultados.curselection()[0]  # Get the current selected index
            titulo = self.listbox_resultados.get(index)
            texto = self.datos[self.usuario_actual]["datos"][titulo]
            messagebox.showinfo(titulo, texto)
        except IndexError:
            pass  # Do nothing if there's no selection or index is out of range

    # Form for adding a new query
    def formulario_añadir_consulta(self):
        self.ventana_añadir = Toplevel(self.root)
        self.ventana_añadir.title("Añadir consulta")

        tk.Label(self.ventana_añadir, text="Título:").pack()
        self.entry_titulo_nuevo = tk.Entry(self.ventana_añadir)
        self.entry_titulo_nuevo.pack()

        tk.Label(self.ventana_añadir, text="Texto e Imágenes:").pack()
        self.texto_nuevo = tk.Text(self.ventana_añadir, height=10, width=50)
        self.texto_nuevo.pack()

        tk.Button(self.ventana_añadir, text="Guardar", command=self.guardar_nueva_consulta).pack()
        tk.Button(self.ventana_añadir, text="Insertar Imagen", command=self.insertar_imagen).pack()

    # Save the new query to the user's data
    def guardar_nueva_consulta(self):
        titulo = self.entry_titulo_nuevo.get()
        texto = self.texto_nuevo.get("1.0", tk.END)

        # Check if the title and text are not empty
        if titulo and texto.strip():
            if titulo in self.datos[self.usuario_actual]["datos"]:
                messagebox.showerror("Error", "Ya existe una consulta con ese título.")
            else:
                self.datos[self.usuario_actual]["datos"][titulo] = texto
                self.guardar_datos(self.datos)  # Save the updated data
                messagebox.showinfo("Éxito", "Consulta añadida correctamente.")
                self.ventana_añadir.destroy()
        else:
            messagebox.showerror("Error", "Título y texto son requeridos.")
    # Unused method for adding simple text information through dialogs
    def añadir_informacion(self):
        titulo = simpledialog.askstring("Añadir", "Título:")
        texto = simpledialog.askstring("Añadir", "Texto:")

        # Check if both title and text have been provided
        if titulo and texto:
            # Add the new information under the current user's data
            self.datos[self.usuario_actual]["datos"][titulo] = texto
            # Save the updated data
            self.guardar_datos(self.datos)
            messagebox.showinfo("Añadir", "Información añadida exitosamente")
        else:
            # Show error message if either title or text is missing
            messagebox.showerror("Añadir", "Tanto el título como el texto son necesarios.")

    # Method to search for information based on the query entered in the search box
    def buscar_informacion(self):
        consulta = self.entry_buscar.get()
        resultados = ""

        # Search for matching titles in the current user's data
        if consulta:
            for titulo, texto in self.datos[self.usuario_actual]["datos"].items():
                if consulta.lower() in titulo.lower():
                    resultados += f"Título: {titulo}\nTexto: {texto}\n\n"

            # Display the search results or a message if no results were found
            if resultados:
                messagebox.showinfo("Resultados", resultados)
            else:
                messagebox.showinfo("Buscar", "No se encontraron resultados.")

    # Method to save the encrypted data to a file
    def guardar_datos(self, datos):
        datos_json = json.dumps(datos, ensure_ascii=False).encode('utf-8')
        datos_encriptados = fernet.encrypt(datos_json)
        with open(archivo_datos, "wb") as archivo:
            archivo.write(datos_encriptados)

    # Method to load and decrypt data from a file
    def cargar_datos(self):
        if os.path.exists(archivo_datos):
            with open(archivo_datos, "rb") as archivo:
                datos_encriptados = archivo.read()
                try:
                    datos_json = fernet.decrypt(datos_encriptados)
                    return json.loads(datos_json.decode('utf-8'))
                except Exception as e:
                    print(f"Error al desencriptar los datos: {e}")
                    return {}
        else:
            return {}

    # Method to insert an image into the new query form
    def insertar_imagen(self):
        ruta_imagen = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if ruta_imagen:
            try:
                img = Image.open(ruta_imagen)
                foto = ImageTk.PhotoImage(img)
                self.texto_nuevo.image_create(tk.END, image=foto)
                self.texto_nuevo.image = foto  # Keep a reference to avoid garbage collection
                self.texto_nuevo.insert(tk.END, '\n' + ruta_imagen)  # Optional: append the image path
            except Exception as e:
                print(f"No se pudo cargar la imagen: {e}")

    # Method to delete a selected query
    def borrar_consulta(self):
        try:
            index = self.listbox_resultados.curselection()[0]
            titulo = self.listbox_resultados.get(index)
            if messagebox.askyesno("Confirmar", f"¿Borrar consulta '{titulo}'?"):
                del self.datos[self.usuario_actual]["datos"][titulo]
                self.guardar_datos(self.datos)
                self.actualizar_sugerencias(None)  # Refresh the list of queries
                messagebox.showinfo("Borrado", "Consulta borrada correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione una consulta para borrar.")

    # Method to open the editing form for an existing query
    def editar_consulta(self):
        try:
            index = self.listbox_resultados.curselection()[0]
            titulo_seleccionado = self.listbox_resultados.get(index)
            texto_seleccionado = self.datos[self.usuario_actual]["datos"][titulo_seleccionado]
            self.abrir_ventana_edicion(titulo_seleccionado, texto_seleccionado)
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione una consulta para editar.")
    def abrir_ventana_edicion(self, titulo, texto):
        self.ventana_edicion = tk.Toplevel(self.root)
        self.ventana_edicion.title("Editar Consulta")

        # Display a label and entry for editing the title
        tk.Label(self.ventana_edicion, text="Título:").pack()
        entry_titulo = tk.Entry(self.ventana_edicion)
        entry_titulo.insert(0, titulo)  # Prefill the entry with the current title
        entry_titulo.pack()

        # Display a label and text area for editing the query text
        tk.Label(self.ventana_edicion, text="Texto:").pack()
        texto_edicion = tk.Text(self.ventana_edicion, height=10, width=50)
        texto_edicion.insert("1.0", texto)  # Prefill the text area with the current text
        texto_edicion.pack()

        # Display a button to save the changes, passing the original title, new title, and new text to the handler
        tk.Button(self.ventana_edicion, text="Guardar Cambios", 
                  command=lambda: self.guardar_cambios_consulta(titulo, entry_titulo.get(), texto_edicion.get("1.0", tk.END))).pack()

    # Method to save changes to an existing query
    def guardar_cambios_consulta(self, titulo_original, nuevo_titulo, nuevo_texto):
        # Ensure the new title and text are not empty
        if nuevo_titulo and nuevo_texto.strip():
            # If the title has been changed, remove the original entry
            if nuevo_titulo != titulo_original:
                del self.datos[self.usuario_actual]["datos"][titulo_original]
            # Update the entry with the new title and text
            self.datos[self.usuario_actual]["datos"][nuevo_titulo] = nuevo_texto.strip()
            # Save the updated data
            self.guardar_datos(self.datos)
            # Close the editing window
            self.ventana_edicion.destroy()
            # Refresh the list of queries
            self.actualizar_sugerencias(None)
            messagebox.showinfo("Éxito", "Consulta actualizada correctamente.")
        else:
            messagebox.showerror("Error", "Título y texto son requeridos.")

    # Method to display the details of a query when clicked
    def mostrar_detalle_consulta_con_click(self, event):
        widget = event.widget
        if not widget.curselection():
            index = widget.nearest(event.y)  # Get the index nearest to the mouse click
            widget.selection_clear(0, tk.END)
            widget.selection_set(index)
            widget.event_generate("<<ListboxSelect>>")  # Manually trigger the ListboxSelect event

    # The main block to run the application
if __name__ == "__main__":
        root = tk.Tk()  # Create the main window
        app = BibliotecaApp(root)  # Instantiate the application with the main window
        root.mainloop()  # Start the application's main loop            