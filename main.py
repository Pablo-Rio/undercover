from game import *
from player import *

# Exécution du jeu
if __name__ == "__main__":
    keep_playing = True
    names, players, num_civils, num_undercovers, num_mr_whites = start_game()
    print("Les préparatifs sont terminés. Le jeu commence !\n")
    while keep_playing:
        random.shuffle(players)
        for player in players:
            os.system('cls')
            reveal_secret_word(player)
        partie_en_cours = True
        i : int = 0
        while partie_en_cours:
            print(f"Phase de discussion. C'est à {players[i].name} de commencer.\n")
            eliminated_player = phase_elimination(players)
            if players[i] == eliminated_player:
                i += 1
            partie_en_cours = determine_winner(players)
        keep_playing = input("Souhaitez-vous rejouer ? (O/N) ") in ["O", "o"]
        if keep_playing:
            print("Nouvelle partie !\n")
            players = role_allocation(names, num_civils, num_undercovers, num_mr_whites)
