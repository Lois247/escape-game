import random
import time
import tkinter as tk

x = 2

lettres = ['E', 'S', 'C', 'A', 'P']

sequence = []
user_input = []

def debut_de_la_partie():
    global sequence, user_input
    user_input = []
    sequence.append(random.choice(lettres))
    show_sequence()

def show_sequence():
    print(" ".join(sequence))  # Affiche la séquence
    time.sleep(2)  # Pause de 2 secondes
    print("\n" * 50)  # Simule l'effacement de l'écran

def choix(lettre):
    global sequence, user_input
    user_input.append(lettre)
    if user_input == sequence:
        print("Bravo ! Nouvelle séquence...")
        time.sleep(1)  # Pause avant de continuer
        debut_de_la_partie()
    elif not sequence[:len(user_input)] == user_input:
        print("Perdu ! La séquence était : " + " ".join(sequence))
        sequence.clear()
        print("Tapez 'reset' pour recommencer ou 'quit' pour quitter.")

def reset_game():
    global sequence, user_input
    sequence = [random.choice(lettres)]
    user_input = []
    print("Nouvelle partie !")
    show_sequence()

if str(x) == "2":
    print("Bienvenue dans le jeu de séquence !")
    print("Appuyez sur les lettres dans le bon ordre pour gagner.")
    print("Entrez 'reset' pour recommencer ou 'quit' pour quitter.\n")

    debut_de_la_partie()

    while True:
        # Demande à l'utilisateur d'entrer une lettre
        entree = input("Votre choix (lettre ou 'reset'/'quit') : ").strip().upper()

        if entree == "QUIT":
            print("Merci d'avoir joué ! À bientôt.")
            break
        elif entree == "RESET":
            reset_game()
        elif entree in lettres:
            choix(entree)
        else:
            print("Entrée invalide. Veuillez entrer une lettre valide.")