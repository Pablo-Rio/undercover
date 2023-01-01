import os
import random
from player import Player


def first_game():
    players = []
    while True:
        num_players = input_number("Combien y a-t-il de joueurs ? ")
        if num_players < 3:
            print("Il faut au moins 3 joueurs !")
        else:
            break
    print(f"{num_players} ? Il me faut des noms !")
    i : int = 0
    while i!=num_players:
        while True:
            name = input_string(f"Nom du joueur {i+1} : ")
            if name in [player.name for player in players]:
                print("Ce nom est déjà pris !")
            else:
                break
        players.append(Player(name, i+1))       
        i+=1
        
    entree: str = ''
    while True:
        print("Nombre d' Undercovers et de Mr. Whites...")
        print("1 - aléatoires")
        print("2 - à définir")
        entree = input_string("Choix : ")
        match entree:
            case '1':
                num_civils = random.randint(2, num_players - 1)
                num_undercovers = random.randint(1, num_players - num_civils)
                num_mr_whites = num_players - num_civils - num_undercovers
            case '2':
                while True:
                    num_undercovers = input_number("Combien y a-t-il de Undercovers ? ")
                    if num_undercovers > num_players - 2 or num_undercovers < 1:
                        print(f"Nombre de Undercovers incorrect ! Il en faut entre 1 et {num_players - 2}.")
                    else:
                        break
                while True:
                    num_mr_whites = input_number("Combien y a-t-il de Mr. Whites ? ")
                    if num_mr_whites > num_players - num_undercovers - 1 or num_mr_whites < 0:
                        print(f"Nombre de Mr. Whites incorrect ! Il en faut entre 0 et {num_players - num_undercovers - 2}.")
                    else:
                        break
                num_civils = num_players - num_undercovers - num_mr_whites
            case _:
                print("Erreur : numéro de menu incorrect.")
        if entree in ['1', '2']:
            break
    game_parameters = [num_players, num_civils, num_undercovers, num_mr_whites]
    players = role_allocation(players, game_parameters)
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
    
    players = reset_roles_and_status(players)
  
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
    
    for i in range(game_parameters[3]):
        # On choisit un joueur au hasard, on vérifie qu'il n'est pas déjà Undercover ou Civil, puis on lui met le rôle de Mr. White sans lui donner de mot secret
        number = random.randint(0, len(players) - 1)
        while players[number].role == "Undercover" or players[number].role == "Mr. White":
            number = random.randint(0, len(players) - 1)
        players[number].role = "Mr. White"
        players[number].secret_word = None
    
    # On attribue le mot secret civil aux joueurs qui n'ont pas encore de rôle
    for player in players:
        if player.role == None:
            player.role = "Civil"
            player.secret_word = secret_word_pair[civil_word]
       
        
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


def reset_roles_and_status(players):
    for player in players:
        player.role = None
        player.secret_word = None
        player.is_eliminated = False
    return players


def phase_elimination(players):
    while True:
        eliminated_player_name = input_string("Pour qui souhaitez-vous voter ? ")
        if eliminated_player_name in [player.name for player in players]:
            break
        else:
            print("Erreur : ce joueur n'existe pas.")
    eliminated_player = next(player for player in players if player.name == eliminated_player_name)
    eliminated_player.eliminate()
    print(f"{eliminated_player.name} était un(e) {eliminated_player.role} !")
    return eliminated_player, players
    

def determine_winner(players):
    num_civils = 0
    num_undercovers = 0
    num_mr_whites = 0
    for player in players:
        if player.role == "Civil":
            civil_secret_word = player.secret_word
    for player in players:
        if player.role == "Civil" and not player.is_eliminated:
            num_civils += 1
        elif player.role == "Undercover" and not player.is_eliminated:
            num_undercovers += 1
        elif player.role == "Mr. White":
            if not player.is_eliminated:
                num_mr_whites += 1
            # Si Mr. White a deviné le mot secret des Civils, alors Mr. White a gagné
            elif player.secret_word == civil_secret_word and player.is_eliminated:
                print("Mr. White a gagné !")
                # Donne 6 points à Mr. White
                for player in players:
                    if player.role == "Mr. White":
                        player.score += 6
                return False
            else:
                print("Raté ! Mr. White a été éliminé.")
    
    # print("Test : il reste", num_civils, "Civils,", num_undercovers, "Undercovers et", num_mr_whites, "Mr. White.")
    
    if num_civils == 1 and num_mr_whites == 0 and num_undercovers > 0:
        print("Les Undercovers ont gagné !")
        # Donne 10 points aux Undercovers
        for player in players:
            if player.role == "Undercover":
                player.score += 10
        return False
    elif num_undercovers == 0 and num_civils == 1 and num_mr_whites > 0:
        print("Mr. White a gagné !")
        # Donne 6 points à Mr. White
        for player in players:
            if player.role == "Mr. White":
                player.score += 6
        return False
    # Si tous les Imposteurs ont été éliminés, alors les Civils ont gagné
    elif num_undercovers == 0 and num_mr_whites == 0:
        print("Les Civils ont gagné !")
        # Donne 2 points aux Civils
        for player in players:
            if player.role == "Civil":
                player.score += 2
        return False
    else:
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

def input_number(message):
    while True:
        # Si l'entrée n'est pas un nombre, on recommence
        try:
            entree = int(input(message))
        except ValueError:
            print("Erreur : vous devez entrer un nombre.")
            continue
        if entree != "":
            break
    return entree

def input_string(message):
    while True:
        entree = input(message)
        if entree != "":
            break
    return entree