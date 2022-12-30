import os
import random
from player import Player


def start_game():
    num_players = int(input("Combien y a-t-il de joueurs ? "))
    print(f"{num_players} ? Il me faut des noms !")
    i : int = 0
    names = []
    while i!=num_players:
        names.append(input(f"Nom du joueur {i+1} : "))
        i+=1
    
    entree: str = ''
    print("Nombre de civils/undercovers/mr whites...")
    print("1 - aléatoires")
    print("2 - à définir")
    entree = input("Choix : ")
    while True:
        match entree:
            case '1':
                num_civils = random.randint(2, num_players - 1)
                num_undercovers = random.randint(1, num_players - num_civils)
                num_mr_whites = num_players - num_civils - num_undercovers
            case '2':
                num_civils = int(input("Combien y a-t-il de Civils ? "))
                num_undercovers = int(input("Combien y a-t-il de Undercovers ? "))
                num_mr_whites = int(input("Combien y a-t-il de Mr. Whites ? "))
            case _:
                print("Erreur : numéro de menu incorrect.")
        if entree in ['1', '2']:
            break

    players = role_allocation(names, num_civils, num_undercovers, num_mr_whites)
    return names, players, num_civils, num_undercovers, num_mr_whites


def role_allocation(names, num_civils, num_undercovers, num_mr_whites):
    players = []
    with open("used_secret_words.txt", "r") as f:
        lines = f.readlines()
    used_secret_words = [line.strip().split(";") for line in lines]
    
    # On récupère la liste des mots secrets
    with open("secret_words.txt", "r") as f:
        lines = f.readlines()
    secret_words = [line.strip().split(";") for line in lines]
    if len(secret_words) == 0:
        print("Il n'y a plus de mot secret disponible ! Il faut en ajouter dans le fichier 'secret_words.txt'.")
        os._exit(0)
  
    secret_word_pair = secret_words[random.randint(0, len(secret_words) - 1)]
    for i in range(num_undercovers):
        name_undercover = names[random.randint(0,3)]
        while name_undercover in [player.name for player in players]:
            name_undercover = names[random.randint(0,3)]
        first_or_second_word = random.randint(0,1)
        players.append(Player(name_undercover, "Undercover", secret_word = secret_word_pair[first_or_second_word]))
    if first_or_second_word == 0:
        first_or_second_word = 1
    else:
        first_or_second_word = 0
    for i in range(num_civils):
        name_civil = names[random.randint(0,3)]
        while name_civil in [player.name for player in players]:
            name_civil = names[random.randint(0,3)]
        players.append(Player(name_civil,"Civil", secret_word = secret_word_pair[first_or_second_word]))
    for i in range(num_mr_whites):
        players.append(Player("Mr. White", None))
        
    # Déplacer le mot secret utilisé dans le fichier "used_secret_words.txt"
    with open("used_secret_words.txt", "a") as f:
        f.write(secret_word_pair[0] + ";" + secret_word_pair[1] + "\n")
    # Supprimer le mot secret utilisé du fichier
    with open("secret_words.txt", "w") as f:
        for line in lines:
            if line.strip('\n') != secret_word_pair[0] + ";" + secret_word_pair[1]:
                f.write(line)

    random.shuffle(players)
    return players


def phase_elimination(players):
    eliminated_player_name = input("Pour qui souhaitez-vous voter ? ")
    eliminated_player = next(player for player in players if player.name == eliminated_player_name)
    eliminated_player.eliminate()
    print(f"{eliminated_player.name} était un {eliminated_player.role} !")
    return eliminated_player
    

def determine_winner(players):
    num_civils = 0
    num_undercovers = 0
    num_mr_whites = 0
    for player in players:
        if player.role == "Civil" and not player.is_eliminated:
            num_civils += 1
        elif player.role == "Undercover" and not player.is_eliminated:
            num_undercovers += 1
        elif player.role == "Mr. White" and not player.is_eliminated:
            num_mr_whites += 1
    if num_civils == 1 and num_undercovers > 0:
        print("Les Undercovers ont gagné !")
        return False
    elif num_undercovers == 0 and num_mr_whites > 0:
        print("Mr. White a gagné !")
        return False
    elif num_undercovers == 0 and num_civils > 0:
        print("Les Civils ont gagné !")
        return False
    else :
        print("La partie continue.")
        return True
    
def reveal_secret_word(player):
    print(f"{player.name}, votre mot secret est...")
    input("")
    print('\033[31m' + player.secret_word.upper() + '\033[0m')
    input("Appuyez sur une touche pour cacher le mot secret...")
    os.system('cls')
    print("Mot secret caché.\n")
