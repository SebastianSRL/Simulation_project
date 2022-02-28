import numpy as np


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.position = 0
        self.jail = False
        self.bankrupt = False

    def turn(self, move, board, players):
        """
        Initialize a player given the name and the initial money.

        :param move: Player's movement
        :param board: Player's board
        :param players: List of players
        """
        board_size = len(board)

        if self.position + move >= board_size:  # Altera la posicion del jugador teniendo en cuenta si ya va a dar una vuelta o no
            move = move - (board_size - self.position)
            self.position = move
        else:
            self.position += move

        standing = board[self.position - 1]  # Propiedad sobre la cual ahora se encuentra situado el jugador

        if standing.owner is None:  # Si la propiedad no tiene dueño
            if standing.value <= self.money:  # Si tiene dinero para comprarla
                self.money -= standing.value
                standing.set_owner(self.name)
        else:  # Si tiene dueño
            if standing.fee <= self.money:
                for player in players:
                    if standing.owner == player.name and player.name != self.name:  # Busca el dueño y que no sea uno mismo
                        self.money -= standing.fee  # Paga
                        player.money += standing.fee
            else:  # Si no puede pagar: bancarrota
                self.bankrupt = True


# No usado en la versión actual
class Bank:
    def __init__(self, money=np.inf):
        self.money = money

    def give_money(self, cash):

        if self.money > 0:
            if self.money > cash:
                loan = cash
                self.money -= cash
            else:
                loan = self.money
                self.money = 0
        else:
            loan = 0

        return loan

    def get_money(self, cash):
        self.money += cash


class Property:
    def __init__(self, name, value, fee):
        self.value = value
        self.fee = fee
        self.position = 0
        self.owner = None

    def set_owner(self, owner):
        """
        Set the owner of the property.
        :param owner:
        """
        self.owner = owner
