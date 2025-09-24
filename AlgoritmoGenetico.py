import numpy as np
import tkinter as tk
from PIL import Image,ImageTk

class algoritmoGenetico:
    def __init__(self, poblacion_frame):
        self.poblacion_frame = poblacion_frame
        self.poblacion = self.generar_poblacion()

        print(len(self.poblacion))

        self.cargar_imagenes_en_interfaz()
      

        
    def generar_poblacion(self):
        poblacion = []
        for i in range(8):
            poblacion.append(self.generar_ruido())
        return poblacion

    def generar_ruido(self):
        # Genera una matriz con valores aleatorios entre 0 y 255
        ruido = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        # img = Image.fromarray(ruido, mode="RGB")
        return ruido
    
    def generar_imagen_desde_array(self,array):

        img = Image.fromarray(array, mode="RGB")
        # img.show()
        return ImageTk.PhotoImage(img)
    
    def cargar_imagenes_en_interfaz(self):
        img_labels = []
        i = 0
        for arrayImg in self.poblacion:
            img = self.generar_imagen_desde_array(arrayImg)
            img_labels.append(tk.Label(self.poblacion_frame, image=img))
            img_labels[i].image = img

            if i < 4:
                img_labels[i].grid(row=0, column=i)
            else:
                img_labels[i].grid(row=1, column=i-4)

            i+=1

    


# # Ejemplo: ruido de 256x256 píxeles
# imagen_ruido = generar_ruido()
# imagen_ruido.show()         # Mostrar en pantalla
# imagen_ruido.save("ruido.png")  # Guardar como archivo
