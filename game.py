import os
import random
from player import Player


def first_game():
    players = []
    num_players = int(input("Combien y a-t-il de joueurs ? "))
    print(f"{num_players} ? Il me faut des noms !")
    i : int = 0
    while i!=num_players:
        players.append(Player(input(f"Nom du joueur {i+1} : "), i+1))       
        i+=1
        
    entree: str = ''
    print("Nombre de civils/undercovers/mr whites...")
    print("1 - aléatoire")
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
    game_parameters = [num_players, num_civils, num_undercovers, num_mr_whites]
    role_allocation(players, game_parameters)
    return players, game_parameters


def role_allocation(players, game_parameters):
    random.shuffle(players)
    # On récupère la liste des mots secrets
    with open("secret_words.txt", "r") as f:
        lines = f.readlines()
    secret_words = [line.strip().split(";") for line in lines]
    if len(secret_words) == 0:
        print("Il n'y a plus de mot secret disponible ! Il faut en ajouter dans le fichier 'secret_words.txt'.")
        os._exit(0)
    
    players = reset_roles(players)
  
    secret_word_pair = secret_words[random.randint(0, len(secret_words) - 1)]
    undercover_word = random.randint(0,1)
    for i in range(game_parameters[2]):
        # On choisit un joueur au hasard et on lui met le rôle d'Undercover et le mot secret
        number = random.randint(0, len(players) - 1)
        players[number].role = "Undercover"
        players[number].secret_word = secret_word_pair[undercover_word]
        
    if undercover_word == 0:
        civil_word = 1
    else:
        civil_word = 0
        
        
    for i in range(game_parameters[1]):
        # On choisit un joueur au hasard, on vérifie qu'il n'est pas déjà Undercover, puis on lui met le rôle de civil et le mot secret associé
        number = random.randint(0, len(players) - 1)
        while players[number].role == "Undercover" or players[number].role == "Civil":
            number = random.randint(0, len(players) - 1)
        players[number].role = "Civil"
        players[number].secret_word = secret_word_pair[civil_word]
        
    for i in range(game_parameters[3]):
        # On choisit un joueur au hasard, on vérifie qu'il n'est pas déjà Undercover ou Civil, puis on lui met le rôle de Mr. White sans lui donner de mot secret
        number = random.randint(0, len(players) - 1)
        while players[number].role == "Undercover" or players[number].role == "Civil" or players[number].role == "Mr. White":
            number = random.randint(0, len(players) - 1)
        players[number].role = "Mr. White"
        players[number].secret_word = None
        
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


def reset_roles(players):
    for player in players:
        player.role = None
    return players


def phase_elimination(players):
    while True:
        eliminated_player_name = input("Pour qui souhaitez-vous voter ? ")
        if eliminated_player_name in [player.name for player in players]:
            break
        else:
            print("Erreur : ce joueur n'existe pas.")
    eliminated_player = next(player for player in players if player.name == eliminated_player_name)
    eliminated_player.eliminate()
    print(f"{eliminated_player.name} était un(e) {eliminated_player.role} !")
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
        # Donne 10 points aux Undercovers
        for player in players:
            if player.role == "Undercover":
                player.score += 10
        return False
    elif num_undercovers == 0 and num_mr_whites > 0:
        print("Mr. White a gagné !")
        # Donne 6 points à Mr. White
        for player in players:
            if player.role == "Mr. White":
                player.score += 6
        return False
    elif num_undercovers == 0 and num_civils > 0:
        print("Les Civils ont gagné !")
        # Donne 2 points aux Civils
        for player in players:
            if player.role == "Civil":
                player.score += 2
        return False
    else :
        print("La partie continue.")
        return True
    
def reveal_secret_word(players):
    os.system('cls')
    # On affiche le mot secret du joueur dans l'ordre croissant de son numéro
    number = 1
    print("Voici le mot secret de chaque joueur :")
    while number <= len(players):
        for player in players:
            if player.number == number:
                print(f"\033[36m{player.name}\033[0m, votre mot secret est...")
                input("")
                if player.role == "Mr. White":
                    print("\033[31m" + "Vous êtes Mr. White !" + "\033[0m")
                else:
                    # print(player.name, "était un(e)", player.role, player.number,player.secret_word)
                    print('\033[31m' + player.secret_word.upper() + '\033[0m')
                input("Appuyez sur une touche pour cacher le mot secret...")
                os.system('cls')
                print("Mot secret caché.\n")
                number += 1
                

def score(players):
    os.system('cls')
    # On affiche le score de chaque joueur dans l'ordre croissant des numéros
    number = 1
    print("Voici le score de chaque joueur :")
    while number <= len(players):
        for player in players:
            if player.number == number:
                print(f"{player.name} : {player.score} point(s)")
                number += 1
    input("Appuyez sur une touche pour continuer...")
    os.system('cls')
