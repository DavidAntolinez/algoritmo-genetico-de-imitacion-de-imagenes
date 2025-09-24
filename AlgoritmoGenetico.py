import numpy as np
import tkinter as tk
from PIL import Image,ImageTk
import threading
import gc

class algoritmoGenetico:
    def __init__(self, poblacion_frame, generacion_label,porcentaje_objetivo, img_original):
        self.poblacion_frame = poblacion_frame
        self.poblacion = self.generar_poblacion()
        self.generacion = 0
        self.generacion_label = generacion_label
        self.porcentaje_objetivo = porcentaje_objetivo
        self.porcentaje_actual = 0
        self.porcentaje_actual_label = tk.Label(poblacion_frame, text="porcentaje de parentezco 0%")
        self.porcentaje_actual_label.grid(row=3, column=3)
        img = np.array(img_original)
        if img.shape[-1] == 4:
            img = img[:, :, :3]
        self.img_original_array = img
        self.padres = []

        

        self.cargar_imagenes_en_interfaz()

        self.iniciar_algoritmo()
       
      

        
    def generar_poblacion(self):
        poblacion = []
        for i in range(8):
            poblacion.append(self.generar_ruido())
        return poblacion

    def generar_ruido(self):
        # Genera una matriz con valores aleatorios entre 0 y 255
        ruido = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        
        return ruido
    
    def generar_imagen_desde_array(self,array):

        img = Image.fromarray(array, mode="RGB")

        self.img_tk = ImageTk.PhotoImage(img)
        
        return self.img_tk
    
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

    def funcion_objetivo(self,img1,img2):

        # Normalizar a RGB (3 canales)
        if img1.shape[-1] == 4:
            img1 = img1[:, :, :3]  # descartar alfa
        if img2.shape[-1] == 4:
            img2 = img2[:, :, :3]

        iguales = np.sum(img1 == img2)
        total = img1.size
        similitud = iguales / total * 100
        return similitud
    
    def detener_algoritmo(self):
        if self.porcentaje_actual >= self.porcentaje_objetivo:
            return False
        return True

    def buscar_padres(self):
        poblacion_ordenada = sorted(
        self.poblacion,
        key=lambda img: self.funcion_objetivo(self.img_original_array, img),
        reverse=True
        )   
        self.padres = []
        self.padres.append(poblacion_ordenada.pop())
        self.padres.append(poblacion_ordenada.pop())
    
    def nuevo_porcentaje_actual(self):
        padres_ordenados = sorted(
        self.padres,
        key=lambda img: self.funcion_objetivo(self.img_original_array, img),
        reverse=True
        )   
        self.porcentaje_actual = self.funcion_objetivo(self.img_original_array, padres_ordenados.pop())
        self.porcentaje_actual_label.config(text=f'porcentaje de parentezco {self.porcentaje_actual:.3}%')

    def nueva_generacion(self):
        self.generacion += 1
        self.generacion_label.config(text=f'Poblacion: generacion {self.generacion}')

    def mutacion(self, img):
        mask = np.random.rand(*img.shape[:2], 1) < 0.5
        condicion = mask & (img != self.img_original_array)
        img[condicion] = np.random.randint(0, 256, size=np.sum(condicion), dtype=np.uint8)
        return img
    

    def cruce(self):
        mask = np.random.rand(*self.padres[0].shape[:2], 1) > 0.5
        hijo = np.where(mask, self.padres[0], self.padres[1])
        hijo[self.img_original_array == self.padres[0]] = self.padres[0][self.img_original_array == self.padres[0]]
        hijo[self.img_original_array == self.padres[1]] = self.padres[1][self.img_original_array == self.padres[1]]
        return hijo.astype(np.uint8)

    def iniciar_algoritmo(self):
        hilo = threading.Thread(target=self.algoritmo_genetico, daemon=True)
        hilo.start()
        

    def algoritmo_genetico(self):

        while self.detener_algoritmo():

            self.buscar_padres()

            self.poblacion = [self.cruce() for img in self.poblacion]
            self.poblacion = [self.mutacion(img) for img in self.poblacion]
        
            self.nuevo_porcentaje_actual()

            self.nueva_generacion()

            self.cargar_imagenes_en_interfaz()
