import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial 
import threading
import os
import subprocess

serial_port = serial.Serial(port = "/dev/ttyUSB0", baudrate = 38400)



def ajuster_luminosite(valeur, base_color):
    luminosite = int(valeur)

#Obtenir les valeurs RGB de la couleur de base
    r, g, b = window.winfo_rgb(base_color)

#Convertir ces valeurs en pourcentage
    r = int((r / 65535) * luminosite)
    g = int((g / 65535) * luminosite)
    b = int((b / 65535) * luminosite)

#Recréer la couleur ajustée
    couleur = f'#{r:02x}{g:02x}{b:02x}'

#Appliquer la nouvelle couleur de fond
    window.config(bg=couleur)
    color_frame.config(bg=couleur)
    bottom_frame.config(bg = couleur)
    scrollbar_luminos.config(bg = couleur)
    scrollbar_volume.config(bg = couleur)
    label_image_vol.config(bg = couleur)
    label_image_lum.config(bg = couleur)

# Fonction pour changer la couleur de fond
def change_bg(color):
    window.config(bg=color)
    color_frame.config(bg=color)
    bottom_frame.config(bg = color)
    scrollbar_luminos.config(bg = color)
    scrollbar_volume.config(bg = color)
    label_image_lum.config(bg = color)
    label_image_vol.config(bg = color)

    current_color[0] = color
    ajuster_luminosite(scrollbar_luminos.get(), current_color)

# Fonction pour afficher une alerte avec les stats
def show_stats():
    messagebox.showinfo("Statistiques", "Voici vos statistiques.")

# Fonction pour ouvrir les paramètres
def show_settings():
    messagebox.showinfo("Paramètres", "Voici les paramètres de l'application.")

# Fonction pour se déconnecter
def logout():
    window.quit()

# Fonction pour afficher le menu déroulant du profil
def show_profile_menu(event):
    profile_menu.tk_popup(event.x_root, event.y_root)

# Fonction pour lancer un jeu (vous remplacerez cette fonction par l'appel à votre programme PyGame)
def launch_game():
    logout()
    result = subprocess.run(["python3", "media/sb/SB/mainSB.py"], capture_output=True, text=True)

    

    
def detect_usb_drives(file_name):
    base_dirs = ["/media", "mnt"]
    
    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            for item in os.listdir(base_dir):
                full_path = os.path.join(base_dir, item)
                if os.path.ismount(full_path):
                    print(f"Recherche dans : {full_path}")
                    for root, dirs, files in os.walk(full_path):
                        if file_name in files:
                            return os.path.join(root, file_name)
    return '/media/sb/SB'
print(detect_usb_drives('mainSB.py'))

def listen_for_arduino():
    while True:
        if serial_port.in_waiting > 0:
            line = serial_port.readline().decode('utf-8').strip()  # Lire la ligne
            print(f"Message reçu: {line}")
            if "Boutton OK" in line:  # Si le message "Boutton OK" est trouvé
                launch_game()
            elif 'red' in line:
                change_bg('red')
            elif 'orange' in line:
                change_bg('orange')
            elif 'yellow' in line:
                change_bg('yellow')
            elif 'green' in line:
                change_bg('green')
            elif 'blue' in line:
                change_bg('blue')
            elif 'purple' in line:
                change_bg('purple')

def detect_usb_and_change_button(button):
    """Détecte les clés USB et change le bouton en image si 'mainSB.py' est trouvé."""
    while True:
        fichier = False
        from string import ascii_uppercase
        drives = detect_usb_drives('mainSB.py')
        if drives != None:
            change_button_to_image(os.path.join(drives, "jeu.png"))
            return
        else:
            button.config(bg = 'white', text = 'Veuillez insérer un jeu', compound=tk.CENTER)
            return
'''
        usb_drives = [drive for drive in drives]
        for drive in usb_drives:
            potential_file = os.path.join(drive, "mainSB.py")
            if os.path.exists(potential_file):
                fichier = True
                print(f"Fichier trouvé : {potential_file}")
                change_button_to_image(os.path.join(drive, "jeu.png"))
                return 
        if not fichier:
            button.config(bg = 'white', text = 'Veuillez insérer un jeu', compound=tk.CENTER)
            return'''

def change_button_to_image(image_path):
    """Remplace le bouton principal par une image."""
    try:
        # Charger l'image
        img = Image.open(image_path)
        img = img.resize((1000, 600))  # Redimensionner l'image au besoin
        button_image = ImageTk.PhotoImage(img)

        # Mettre à jour le bouton avec l'image
        big_button.config(image=button_image, text="", compound=tk.CENTER, height=600, width=1000)
        big_button.image = button_image  # Prévenir le garbage collection
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'afficher l'image : {e}")


# Créer la fenêtre principale
window = tk.Tk()
window.title("Interface avec menu déroulant")
window.attributes("-fullscreen", True)
window.config(bg = 'purple')

current_color = ['purple']

# Créer un cadre pour les boutons de changement de couleur, et le placer au centre en haut
color_frame = tk.Frame(window)
color_frame.pack(side=tk.TOP, pady=0)
color_frame.config(bg='purple')


# Ajouter des boutons pour changer la couleur du fond, et les aligner horizontalement dans le cadre
button_red = tk.Button(color_frame, text="",bg = 'red', command=lambda: change_bg("red"), height=5, width=12)
button_red.pack(side=tk.LEFT, padx=(270, 30))

button_orange = tk.Button(color_frame, text="",bg = 'orange', command=lambda: change_bg("orange"), height=5, width=12)
button_orange.pack(side=tk.LEFT, padx=30)

button_yellow = tk.Button(color_frame, text="",bg = 'yellow', command=lambda: change_bg("yellow"), height=5, width=12)
button_yellow.pack(side=tk.LEFT, padx=30)

button_green = tk.Button(color_frame, text="",bg = 'green', command=lambda: change_bg("green"), height=5, width=12)
button_green.pack(side=tk.LEFT, padx=30)

button_blue = tk.Button(color_frame, text="",bg = 'blue', command=lambda: change_bg("blue"), height=5, width=12)
button_blue.pack(side=tk.LEFT, padx=30)

button_purple = tk.Button(color_frame, text="",bg = 'purple', command=lambda: change_bg("purple"), height=5, width=12)
button_purple.pack(side=tk.LEFT, padx=30)

# Créer un menu déroulant pour le profil
profile_menu = tk.Menu(window, tearoff=0)
profile_menu.add_command(label="Stat", command=show_stats)
profile_menu.add_command(label="Paramètre", command=show_settings)
profile_menu.add_command(label="Déconnexion", command=logout)


button_profile = tk.Button(color_frame, text="Profil", height=5, width=12)
button_profile.pack(side=tk.LEFT, padx=(270, 0))
button_profile.bind("<Button-1>", show_profile_menu)

# Créer un bouton pour lancer le jeu (prend la majeure partie de l'écran)
big_button = tk.Button(window, text="Veuillez insérer un jeu", command=launch_game, font=("Helvetica", 24), height=15, width=60)
big_button.pack(expand=True)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side = tk.BOTTOM, pady = 0)
bottom_frame.config(bg = 'purple')


image_lum = Image.open('img/luminos1.png')
image_lum = ImageTk.PhotoImage(image_lum)  # Convertir l'image en format compatible Tkinter
label_image_lum = tk.Label(bottom_frame, image=image_lum, bg = 'purple')
label_image_lum.pack(side=tk.LEFT, padx=(20, 0))
#Curseur pour ajuster la luminosité
scrollbar_luminos = tk.Scale(bottom_frame, from_=0, to=255, orient=tk.HORIZONTAL,showvalue=False, command=lambda val: ajuster_luminosite(val, current_color))
scrollbar_luminos.pack(side=tk.LEFT,padx = 10, ipadx = 250)

scrollbar_luminos.set(128)  # Initialiser la luminosité à 128


image_vol = Image.open('img/volume1.png')
image_vol = ImageTk.PhotoImage(image_vol)  # Convertir l'image en format compatible Tkinter
label_image_vol = tk.Label(bottom_frame, image=image_vol, bg = 'purple')
label_image_vol.pack(side=tk.LEFT, padx=(20, 0))
#Curseur pour ajuster la luminosité
scrollbar_volume = tk.Scale(bottom_frame, from_=0, to=255,showvalue=False, orient=tk.HORIZONTAL)
scrollbar_volume.pack(side=tk.LEFT,padx = 10,  ipadx = 250)

scrollbar_volume.set(128)  # Initialiser la luminosité à 128


# Lancer la boucle d'écoute dans un thread séparé
thread_arduino = threading.Thread(target=listen_for_arduino)
thread_arduino.daemon = True  # Assurer que le thread se termine lorsque le programme se termine
thread_arduino.start()

thread_USB = threading.Thread(target=detect_usb_and_change_button(big_button))
thread_USB.daemon = True  # Assurer que le thread se termine lorsque le programme se termine
thread_USB.start()


# Lancer la boucle principale
window.mainloop()
