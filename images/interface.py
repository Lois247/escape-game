import random
import tkinter as tk

lettres = ['E', 'S', 'C', 'A', 'P']

sequence = []
user_input = []
perdu = False  # Ajout de l'état pour savoir si on a perdu

def debut_de_la_partie():
    global sequence, user_input, perdu
    if perdu:  # Si on a perdu, ne commence pas une nouvelle séquence.
        return
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

def show_sequence():
    titre.config(text="Séquence : " + " ".join(sequence))
    root.after(2000, lambda: titre.config(text="Reproduis la séquence..."))

def choix(lettre):
    global sequence, user_input, perdu
    if perdu:  # Si on a perdu, on ne fait rien.
        return

    user_input.append(lettre)
    if user_input == sequence:
        titre.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        titre.config(text="Perdu ! La séquence était : " + " ".join(sequence) + "\nClique sur Reset ou Quitter.")
        perdu = True  # On marque que le joueur a perdu

def reset_game():
    global sequence, user_input, perdu
    sequence = []
    user_input = []
    perdu = False  # Réinitialisation de l'état de la défaite
    debut_de_la_partie()  # Relancer une nouvelle séquence

# Interface Tkinter
root = tk.Tk()
root.title("Jeu de séquence")
root.geometry("350x250")

titre = tk.Label(root, text="Bienvenue dans le jeu de séquence !", font=("Arial", 12))
titre.pack(pady=10)

# Boutons lettres
frame_lettres = tk.Frame(root)
frame_lettres.pack(pady=10)

for lettre in lettres:
    bouton = tk.Button(frame_lettres, text=lettre, width=4, height=2, font=("Arial", 12),
                       command=lambda l=lettre: choix(l))
    bouton.pack(side=tk.LEFT, padx=5)

# Boutons reset et quitter
frame_control = tk.Frame(root)
frame_control.pack(pady=20)

btn_reset = tk.Button(frame_control, text="Reset", command=reset_game)
btn_reset.pack(side=tk.LEFT, padx=20)

btn_quit = tk.Button(frame_control, text="Quitter", command=root.quit)
btn_quit.pack(side=tk.RIGHT, padx=20)

# Lancer le jeu
debut_de_la_partie()

root.mainloop()
