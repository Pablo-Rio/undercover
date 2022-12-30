from game import *
from player import *

# Exécution du jeu
if __name__ == "__main__":
    player_turn_name : str
    current_game : bool
    eliminated_player : Player
    new_game : bool
    keep_playing : bool
    players : list[Player]
    game_parameters : list[int]

    print("Bienvenue dans le jeu Undercover !\n")
    new_game = True
    while new_game:
        new_game = False
        keep_playing = True
        players, game_parameters = first_game()
        print("Les préparatifs sont terminés. Le jeu commence !\n")
        while keep_playing:
            reveal_secret_word(players)
            current_game = True
            
            # Détermine aléatoirement le joueur qui commence
            i : int = random.randint(1, len(players))
            while current_game:
                for player in players:
                    if player.number == i:
                        player_turn_name = player.name
                print(f"Phase de discussion. C'est à {player_turn_name} de commencer.\n")
                eliminated_player = phase_elimination(players)
                # Si le joueur éliminé est le joueur qui devait commencer, on passe au joueur suivant
                if eliminated_player.number == i:
                    i += 1
                    if i > len(players):
                        i = 1
                current_game = determine_winner(players)
            entree: str = ''
            while True:
                print("1 - Rejouer avec les mêmes paramètres")
                print("2 - Rejouer en changeant les paramètres")
                print("3 - Voir les scores")
                print("4 - Quitter")
                entree = input("Choix : ")
                match entree:
                    case '1':
                        print("Nouvelle partie !\n")
                        players = role_allocation(players, game_parameters)
                    case '2':
                        new_game = True
                        keep_playing = False
                    case '3':
                        score(players)
                    case '4':
                        keep_playing = False
                    case _:
                        print("Erreur : numéro de menu incorrect.")
                if entree in ['1', '2', '4']:
                    break
