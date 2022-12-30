class Player:
    def __init__(self, name, role, secret_word):
        self.role = role
        self.name = name
        self.secret_word = secret_word
        self.is_eliminated = False

    def eliminate(self):
        self.is_eliminated = True