import tkinter as tk
import random

label = tk.Label
display = None

# Lettres du jeu
lettres = ['𝖊', '𝖘', '𝖈', '𝖆', '𝖕', '𝖊']
sequence = []
user_input = []

def debut_de_la_partie():
    global sequence, user_input
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

# Fonction pour afficher la séquence
def show_sequence():
    global sequence
    display.config(text=" ".join(sequence))
    root.after(2000, lambda: display.config(text=""))

# Fonction de gestion du clic utilisateur
def user_click(lettre):
    global sequence, user_input
    user_input.append(lettre)
    if user_input == sequence:
        label.config(text="Bravo ! Nouvelle séquence...")
        root.after(1000, debut_de_la_partie)
    elif not sequence[:len(user_input)] == user_input:
        label.config(text="Perdu ! Réessaye.")
        sequence = []

def reset_game():
    global sequence, user_input
    # Réinitialisation de la séquence avec une lettre aléatoire
    sequence = [random.choice(lettres)]
    user_input = []  # Réinitialiser l'entrée de l'utilisateur
    show_sequence()

root = tk.Tk()
root.title("Jeu de Séquence Médiéval")

root.mainloop()

