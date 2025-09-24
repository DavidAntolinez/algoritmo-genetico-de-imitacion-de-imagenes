from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog,messagebox
import re
from AlgoritmoGenetico import algoritmoGenetico

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Imitacion de imagen")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Centrar la ventana
        self.centrar_ventana()
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 1200
        height = 600  
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        image_label = tk.Label(self.root)
        image_label.pack()

        upload_button = tk.Button(self.root, text="Upload Image", command=lambda: self.upload_image(image_label))
        upload_button.pack()
        

        # main_frame = tk.Frame(self.root, bg="white")
        # main_frame.pack(padx=30, fill='both', expand=True)


    def upload_image(self,image_label):
        global img_tk # Use a global variable to prevent garbage collection
        file_path = filedialog.askopenfilename()
        if file_path:
            # Open the image using Pillow
            img = Image.open(file_path)
            
            # Resize the image if needed (optional)
            img = img.resize((200, 200), Image.LANCZOS) # Example resize
            
            # Convert the Pillow image to a Tkinter PhotoImage
            img_tk = ImageTk.PhotoImage(img)

            self.mi_imagen = img_tk
            
            # Update the image on the label
            image_label.config(image=img_tk)
            image_label.image = img_tk # Keep a reference to prevent garbage collection    

            self.crear_campo_entrada(self.root, "porcentaje de parentezco deseado", "porcentaje_var", 2)

            upload_button = tk.Button(self.root, text="Iniciar Algoritmo", command=lambda: self.iniciar_algoritmo())
            upload_button.pack()
            

    def crear_campo_entrada(self, parent, texto, var_name, row):
        """Crea un campo de entrada con validación numérica"""
        
        # Etiqueta
        label = tk.Label(
            parent, 
            text=texto, 
            font=("Arial", 11, "bold"), 
            bg='#f0f0f0', 
            fg='#2c3e50'
        )
        label.pack()
        
        # Variable y validación
        var = tk.StringVar()
        var.trace('w', lambda *args: self.validar_entrada_numerica(var))
        setattr(self, var_name, var)
        
        # Campo de entrada
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=("Arial", 12),
            width=20,
            relief='groove',
            bd=2
        )
        entry.pack()
    
    def validar_entrada_numerica(self, var):
        """Valida que solo se ingresen números y puntos decimales"""
        valor = var.get()
        
        # Permitir cadena vacía
        if valor == "":
            return True
        
        # Validar formato numérico (enteros y decimales)
        if re.match(r'^\d*\.?\d*$', valor):
            return True
        else:
            # Eliminar el último carácter si no es válido
            var.set(valor[:-1])

    def iniciar_algoritmo(self):

        # try:
            porcentaje_str = self.porcentaje_var.get().strip()

            if not porcentaje_str:
                messagebox.showwarning(
                        "Datos Incompletos", 
                        "Por favor, ingrese el porcentaje de parentezco"
                    )
                return

            porcentaje_parentezco = float(porcentaje_str)
            if porcentaje_parentezco < 100 and porcentaje_parentezco > 0:
                self.mostrar_pantalla_alg()
                return
            else:
                messagebox.showwarning(
                        "Error",
                        "El rango permitido para el porcentaje de parentezco es entre 0 y 100 excluyendo el 0 y el 100"
                    )
                return
        
        # except ValueError:
        #     messagebox.showerror(
        #         "Error de Formato", 
        #         "Por favor, ingrese valores numéricos válidos."
        #     )
        # except Exception as e:
        #     messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
    def mostrar_pantalla_alg(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        poblacion_frame = tk.Frame(self.root, width=950,height=450)
        poblacion_frame.grid(column=1, row=0)

        text_label = tk.Label(poblacion_frame, text="Poblacion")
        text_label.grid(row=3, column= 3)

        original_frame = tk.Frame(self.root, width=200,height=200)
        original_frame.grid(column=3, row=0)

        original_img = tk.Label(original_frame, image=self.mi_imagen)
        original_img.pack()

        text_label2 = tk.Label(original_frame, text="Imagen Original")
        text_label2.pack()

        algoritmoGenetico(poblacion_frame)



        

root = tk.Tk()
app = InterfazGrafica(root)
root.mainloop()
