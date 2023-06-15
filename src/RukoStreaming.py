#RukoStremaing.py
#Autores: Mario Vasquez & Yasmin Chan
#Proyecto Final Centro Multimedia
#Licencia: MIT

#------Modulos a utilizar
from tkinter import * #Para interfáz gráfica
from tkinter import filedialog #Lectura de archivos
import webbrowser #Abrir enlaces de internet
import vlc #Reproductor de medios
import os #Funcionalidades del S.O.
from PIL import Image, ImageTk
import customtkinter
import os
import pyudev
import time
import subprocess

import threading
import sys
import termios
import tty

usb = False

# Obtener el directorio actual
current_dir = os.getcwd()

# Cambiar al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


# # Hilo para detectar la tecla de detener
# def detener_reproduccion_thread():
    # while True:
        # if detener_reproduccion():
            # os._exit(0)


# Funcion que detecta usb conectada o no
def device_event_handler(action, device):
    global usb
    if action == 'add':
        # print("Dispositivo conectado:", device)
        usb = True
        tituloLabel.grid(row=0,column=1, padx=10, pady=10, columnspan="5")
        tituloLabel.config(bg="gray7",fg="thistle1", justify="center", font="Roboto 20")
        usbMedia()
        # # Hilo para ejecutar la función usbMedia
        # usb_media_thread = threading.Thread(target=usbMedia)
        # # Inicia el hilo para ejecutar la función usbMedia
        # usb_media_thread.start()
        # # Inicia el hilo para detectar la tecla de detener
        # detener_reproduccion_thread()
    elif action == 'remove':
        # print("Dispositivo desconectado:", device)
        usb = False
        tituloLabel.grid_remove()

# Crear un contexto pyudev
context = pyudev.Context()

# Crear un monitor para eventos de dispositivos USB
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

# Registrar un controlador de eventos para los eventos de dispositivo
observer = pyudev.MonitorObserver(monitor, device_event_handler)
observer.start()

raiz=Tk() #Creamos el widget principal

#--------Configuraciones del widget principal
#raiz.call('wm', 'iconphoto', raiz._w, PhotoImage(file='apple.png'))
raiz.title("Ruko's Multimedia")
raiz.config(bg="gray7") #fondo de la ventana
raiz.config(bd="15")#el grosor de borde
#raiz.config(relief="sunken")#para los bordes
raiz.attributes('-fullscreen',True)#pantalla completa
#raiz.attributes('-zoomed',True)#Fullscreen para pruebas

# Frame del titulo
frameTitulo=Frame(raiz)
frameTitulo.pack()
frameTitulo.config(bg="gray7")

# Frame de la seccion de Video Streaming
frameVideoS=Frame(raiz)
frameVideoS.pack()
frameVideoS.config(bg="gray7")

# Frame de la seccion de Music Streaming
frameMusicS=Frame(raiz)
frameMusicS.pack()
frameMusicS.config(bg="gray7")

# Frame de la seccion de USB MEDIA
frameUSB=Frame(raiz)
frameUSB.pack()
frameUSB.config(bg="gray7")
	

#------Función par abrir enlaces--------
def AbrirPagina(url):
    #webbrowser.open(url)
    cmd = "/usr/bin/chromium-browser --kiosk " + url
    os.system(cmd)


#----------------Buscar ruta en la rasp-----------
def buscar_ruta_usb():
    context = pyudev.Context()
    for device in context.list_devices(subsystem='block', ID_BUS='usb'):
        dev_name = device.device_node
        dev_dir = os.path.join('/media/raspado/', os.path.basename(dev_name))
        if os.path.isdir(dev_dir):
            return dev_dir
    return None


#----------------Detectar tipo archivos-----------
def detectar_archivos_mp4_mp3_jpg(ruta):
    archivos_mp4 = []
    archivos_mp3 = []
    archivos_jpg = []
    for archivo in os.listdir(ruta):
        if archivo.endswith(".mp4"):
            archivos_mp4.append(archivo)
        elif archivo.endswith(".mp3"):
            archivos_mp3.append(archivo)
        elif archivo.endswith(".jpg"):
            archivos_jpg.append(archivo)

    return archivos_mp4, archivos_mp3, archivos_jpg

# Función para reproducir archivo .mp3 con vlc
# Ruta de las bibliotecas de VLC (ajústala según tu sistema)
vlc_path = '/usr/lib/vlc'

# # Función para reproducir archivo .jpg con vlc
# def reproducir_presentacion_jpg(archivos):
    # instancia_vlc = vlc.Instance(f'{vlc_path}')
    # lista_reproduccion = instancia_vlc.media_list_new()

    # for archivo in archivos:
        # archivo_absoluto = os.path.abspath(archivo)
        # media = instancia_vlc.media_new(archivo_absoluto)
        # lista_reproduccion.add_media(media)

    # reproductor = instancia_vlc.media_list_player_new()
    # reproductor.set_media_list(lista_reproduccion)

    # reproductor.play()
    # while reproductor.is_playing():
        # pass

    # reproductor.stop()
    
def reproducir_jpg(archivo):
    instancia_vlc = vlc.Instance()
    reproductor = instancia_vlc.media_player_new()
    archivo_absoluto = os.path.abspath(archivo)
    media = instancia_vlc.media_new(archivo_absoluto)
    reproductor.set_media(media)
    reproductor.play()
    #time.sleep(10)

    while reproductor.get_state() != vlc.State.Ended:
        pass

    reproductor.stop()   

# # Función para reproducir archivo .mp3 con vlc
# def reproducir_mp3(archivo):
    # instancia_vlc = vlc.Instance(f'{vlc_path}')
    # reproductor = instancia_vlc.media_player_new()
    # archivo_absoluto = os.path.abspath(archivo)
    # media = instancia_vlc.media_new(archivo_absoluto)
    # reproductor.set_media(media)

    # # Evento para verificar cuando el archivo ha terminado de reproducirse
    # def fin_reproduccion(event):
        # reproductor.stop()
    
    # # Conecta el evento de fin de reproducción al reproductor
    # evento_manager = reproductor.event_manager()
    # evento_manager.event_attach(vlc.EventType.MediaPlayerEndReached, fin_reproduccion)

    # # Inicia la reproducción
    # reproductor.play()

    # # Espera hasta que se haya terminado la reproducción
    # while True:
        # estado = reproductor.get_state()
        # if estado == vlc.State.Ended or estado == vlc.State.Error:
            # break
        # time.sleep(1)
 
# # Función para detectar la pulsación de teclas
# def detener_reproduccion():
    # def getch():
        # fd = sys.stdin.fileno()
        # old_settings = termios.tcgetattr(fd)
        # try:
            # tty.setraw(sys.stdin.fileno())
            # ch = sys.stdin.read(1)
        # finally:
            # termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # return ch

    # tecla = getch()
    # if tecla == 'q':
        # return True
    # return False

# Función para reproducir archivo .mp3 con vlc
def reproducir_mp3(archivo):
    instancia_vlc = vlc.Instance(f'{vlc_path}')
    reproductor = instancia_vlc.media_player_new()
    archivo_absoluto = os.path.abspath(archivo)
    media = instancia_vlc.media_new(archivo_absoluto)
    reproductor.set_media(media)
    reproductor.play()
    time.sleep(30)
    reproductor.stop()
    
def reproducir_mp4(archivo):
    instancia_vlc = vlc.Instance()
    reproductor = instancia_vlc.media_player_new()
    archivo_absoluto = os.path.abspath(archivo)
    media = instancia_vlc.media_new(archivo_absoluto)
    reproductor.set_media(media)
    reproductor.play()
    #time.sleep(10)

    while reproductor.get_state() != vlc.State.Ended:
        pass

    reproductor.stop()  

def reproducir_todo(archivo):
    instancia_vlc = vlc.Instance()
    reproductor = instancia_vlc.media_player_new()
    archivo_absoluto = os.path.abspath(archivo)
    media = instancia_vlc.media_new(archivo_absoluto)
    reproductor.set_media(media)
    reproductor.play()
    #time.sleep(10)

    while reproductor.get_state() != vlc.State.Ended:
        pass

    reproductor.stop() 

def usbMedia():
    #ruta = buscar_ruta_usb()

    ruta = "/media/raspado/MAYITO/"
    time.sleep(5)
    try:
        archivos_mp4, archivos_mp3, archivos_jpg = detectar_archivos_mp4_mp3_jpg(ruta)

        if archivos_mp4 and not archivos_mp3 and not archivos_jpg:
            # Solo se detectaron archivos .mp4
            print("Acción para archivos .mp4")
            for archivo in archivos_mp4:
                print(archivo)
                reproducir_mp4(os.path.join(ruta, archivo))

        elif archivos_mp3 and not archivos_mp4 and not archivos_jpg:
            # Solo se detectaron archivos .mp3
            print("Acción para archivos .mp3")
            for archivo in archivos_mp3:
                print(archivo)
                reproducir_mp3(os.path.join(ruta, archivo))

        elif archivos_jpg and not archivos_mp4 and not archivos_mp3:
            # Solo se detectaron archivos .jpg
            print("Acción para archivos .jpg")
            for archivo in archivos_jpg:
                print(archivo)
                reproducir_jpg(os.path.join(ruta, archivo))
            # reproducir_presentacion_jpg([os.path.join(ruta, archivo) for archivo in archivos_jpg])

        elif archivos_mp4 and archivos_mp3 and archivos_jpg:
            # Se detectaron archivos .mp4, .mp3 y .jpg
            print("Acción para archivos .mp4, .mp3 y .jpg")
            print("Archivos .mp4:")
            todas = archivos_jpg + archivos_mp3 + archivos_mp4
            for archivo in todas:
                reproducir_jpg(os.path.join(ruta, archivo))
            

        else:
            # No se detectaron archivos .mp4, .mp3 ni .jpg
            print("No se encontraron archivos .mp4, .mp3 ni .jpg")
    except FileNotFoundError:
        pass
        


#----------Título de la ventana-----------
tituloLabel=Label(frameTitulo, text="Ruko's Multimedia")
tituloLabel.grid(row=0,column=1, padx=10, pady=10, columnspan="5")
tituloLabel.config(bg="gray7",fg="purple2", justify="center", font="Roboto 50")

# FRAME VIDEO STREAMING 
#----------Título del frame Video Streaming-----------
tituloLabel=Label(frameVideoS, text="Video Streaming")
tituloLabel.grid(row=0,column=1, padx=10, pady=10, columnspan="5")
tituloLabel.config(bg="gray7",fg="thistle1", justify="center", font="Roboto 20")

#------------Botón de HBO----------------
imgHBO=ImageTk.PhotoImage(Image.open("src/img/hbo.png").resize((150,70)))
botonHBO=customtkinter.CTkButton(master=frameVideoS, image=imgHBO,text=None, command=lambda: AbrirPagina('https://play.hbomax.com/signIn'), fg_color="gray7",hover_color = "gray30")
botonHBO.grid(row=1, column=1)


#------------Botón de Netflix----------------
imgNetflix = ImageTk.PhotoImage(Image.open("src/img/netflix.png").resize((150,70)))
botonNetflix=customtkinter.CTkButton(master=frameVideoS, image=imgNetflix,text=None, command=lambda: AbrirPagina('https://www.netflix.com/mx-en/login'), fg_color="gray7", hover_color = "gray30")
botonNetflix.grid(row=1, column=2)#Se define posición del botón

#------------Botón de Disney Plus----------------
imgDisney=ImageTk.PhotoImage(Image.open("src/img/disney.png").resize((150,70)))
botonDisney=customtkinter.CTkButton(master=frameVideoS, image=imgDisney,text=None, command=lambda: AbrirPagina('https://www.disneyplus.com/es-419/login'), fg_color="gray7", hover_color = "gray30")
botonDisney.grid(row=1, column=3)


# FRAME MUSIC STREAMING 
#----------Título del frame MUSIC Streaming-----------
tituloLabel=Label(frameMusicS, text="Music Streaming")
tituloLabel.grid(row=0,column=1, padx=10, pady=10, columnspan="5")
tituloLabel.config(bg="gray7",fg="thistle1", justify="center", font="Roboto 20")

#------------Botón de YoutubeMusic----------------
imgYTM=ImageTk.PhotoImage(Image.open("src/img/youtube.png").resize((150,70)))
botonYTM=customtkinter.CTkButton(master=frameMusicS, image=imgYTM,text=None, command=lambda: AbrirPagina('https://music.youtube.com'), fg_color="gray7", hover_color = "gray30")
botonYTM.grid(row=1, column=1)

#------------Botón de Spotify----------------
imgSpotify=ImageTk.PhotoImage(Image.open("src/img/spotify.png").resize((150,70)))
botonSpotify=customtkinter.CTkButton(master=frameMusicS, image=imgSpotify,text=None, command=lambda: AbrirPagina('https://open.spotify.com'), fg_color="gray7", hover_color = "gray30")
botonSpotify.grid(row=1, column=2)

#------------Botón de Deezer----------------
imgDeezer=ImageTk.PhotoImage(Image.open("src/img/deezer.png").resize((150,70)))
botonDeezer=customtkinter.CTkButton(master=frameMusicS, image=imgDeezer,text=None, command=lambda: AbrirPagina('https://www.deezer.com/mx/'), fg_color="gray7", hover_color = "gray30")
botonDeezer.grid(row=1, column=3)

# FRAME USB MEDIA
#----------Título del frame USB MEDIA-----------

tituloLabel=Label(frameUSB, text="USB MEDIA")

raiz.mainloop()#Mantiene el programa o interfáz siempre abierta

# Detener la observación de eventos de dispositivo USB
observer.stop()
