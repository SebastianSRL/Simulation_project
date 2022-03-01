import numpy as np


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.earned = money
        self.spend = 0
        self.position = 0
        self.turn_counter = 0
        self.go_counter = 0
        self.__jail = False
        self.__bankrupt = False

    def bankruptcy(self):
        """
        Return the player's state
        :return: bankrupt
        """
        return self.__bankrupt

    def jail(self):
        """
        Set the jail property to True
        """
        self.__jail = True

    def pay(self, amount):
        """
        Pays and register the amount on the total spent by the player
        :param amount: Amount to pay
        :return: None
        """
        self.money -= amount
        self.spend -= amount

    def earn(self, amount):
        """
        Saves and registers the amount on the total earned by the player
        :param amount: Amount to save
        :return: None
        """
        self.money += amount
        self.earned += amount

    def turn(self, move, board, players):
        """
        Initialize a player given the name and the initial money.

        :param move: Player's movement
        :param board: Player's board
        :param players: List of players
        """
        self.turn_counter += 1  # Cuenta el turno jugado o perdido

        if not self.__jail:  # Si no cayó en la carcel previamente juega el turno

            board_size = len(board)

            # ================ #
            #     Movement     #
            # ================ #

            if self.position + move >= board_size:  # Altera la posicion del jugador teniendo en cuenta si ya va a dar una vuelta o no
                move = move - (board_size - self.position)
                self.position = move
                self.go_counter += 1  # Contador de vuetas al tablero
                # self.earn(5)  # Da x cantidad en cada vuelta al tablero
            else:
                self.position += move

            standing = board[self.position - 1]  # Propiedad sobre la cual ahora se encuentra situado el jugador

            # ================ #
            #    Behaviour     #
            # ================ #

            if standing.get_name() == 'GO':  # Si pasa por la salida no hace nada a simple vista
                pass  # El dinero por darle la vuelta al tablero se añade en otra parte
            elif standing.get_name() == 'Jail':
                self.jail()  # Si cae en la carce lo hace perder un turno
            else:

                if standing.get_owner() is None:  # Si la propiedad no tiene dueño
                    if standing.get_value() <= self.money:  # Si tiene dinero para comprarla
                        standing.set_owner(self.name)
                        self.pay(standing.get_value())  # Registro de dinero gastado

                else:  # Si tiene dueño
                    if standing.get_fee() <= self.money:

                        # Busca el dueño y que no sea el mismo jugador
                        for player in players:
                            if standing.get_owner() == player.name and player.name != self.name:
                                self.pay(standing.get_fee())  # Paga
                                player.earn(standing.get_fee())  # Registra las ganancias al jugador correspondiente

                    else:

                        # Habilita todas las propiedades del jugador que entro en bancarrota para ser compradas
                        for prop in board:
                            if prop.get_owner() == self.name and prop.get_name():
                                prop.set_owner(None)

                        # Si no puede pagar: bancarrota
                        self.__bankrupt = True

        else:  # Si cayó en la carcel previamente solo se cambia el atributo para jugar el siguiente turno
            self.__jail = False


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


# Super clase celda
class Cell:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_owner(self):
        pass


# Carcel
class Jail(Cell):
    def __init__(self):
        self.__name = 'Jail'
        super().__init__(self.__name)

    # Hace perder un turno a un jugador
    @staticmethod
    def punish(player):
        player.set_jail()


class Property(Cell):
    def __init__(self, name, value, fee):
        self.__value = value
        self.__fee = fee
        self.__owner = None
        super().__init__(name)

    def get_fee(self):
        return self.__fee

    def get_value(self):
        return self.__value

    def get_owner(self):
        return self.__owner

    def set_owner(self, owner):
        """
        Set the owner of the property.
        :param owner:
        """
        self.__owner = owner
