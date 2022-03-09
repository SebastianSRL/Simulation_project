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
        self.owned_props = []
        self.debt = 0
        self.__jail = False
        self.__bankrupt = False

    def bankruptcy(self):
        """
        Return the player's state
        :return: bankrupt
        """
        return self.__bankrupt

    # Simula el lanzamiento de un dado
    def throw_dice(self):
        """
        Simulates a dice
        :return: the result of throwing a dice
        """
        return np.random.randint(1, 7)

    def jail(self):
        """
        Set the jail property to True
        """
        self.__jail = True

    def compare(self, amount):
        return amount <= self.money

    def pay(self, amount, board, debt=True):
        """
        Pays and register the amount on the total spent by the player
        :param debt:
        :param board:
        :param amount: Amount to pay
        :return: None
        """
        # Si el pago no es voluntario como comprar una propiedad
        if debt:
            # Compara si tiene sufieciente dinero para pagar
            if self.compare(amount):
                # Si tiene, paga
                self.money -= amount
                self.spend -= amount
            else:
                # Si no tiene mira que propiedades tienen menor valor
                save = np.zeros((len(self.owned_props),))
                for i, prop in enumerate(self.owned_props):
                    # Guarda el valor de cada propiedad en un arreglo
                    save[i] = prop.get_value()

                # Se mira si vendiendo todas le alcanza para pagar
                if self.compare(amount - np.sum(save)):
                    # Si le alcanza busca las n propiedades de menor valor suficientes
                    # para pagar la deuda
                    payment = 0
                    order = np.argsort(save).ravel()
                    for j, ord in enumerate(order):
                        payment += save[ord]
                        if self.compare(amount - payment):
                            break

                    # Obtiene el valor de cada una de las propiedades vendidas
                    self.earn(payment)
                    # Se paga la deuda
                    self.money -= amount
                    self.spend -= amount

                    # Se desvincula cada una de las propiedades vendidas del jugador actual
                    for prop in self.owned_props:
                        if prop.get_value() in save[order[:j + 1]]:
                            prop.set_owner(None)
                            self.owned_props.remove(prop)

                else:
                    # Si no puede pagar: bancarrota
                    self.__bankrupt = True
                    self.debt = amount
        else:
            # Si es una compra voluntaria como una propiedad
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

    def movement(self, move, board_size):

        # Altera la posicion del jugador teniendo en cuenta si ya va a dar una vuelta o no
        if self.position + move >= board_size:
            move = move - (board_size - self.position)
            self.position = move
            self.go_counter += 1  # Contador de vuetas al tablero
            # self.earn(5)  # Da x cantidad en cada vuelta al tablero
        else:
            self.position += move

    def turn(self, move, board, players, magic_card=False):
        """
        Initialize a player given the name and the initial money.

        :param move: Player's movement
        :param board: Player's board
        :param players: List of players
        """
        if not magic_card:
            self.turn_counter += 1  # Cuenta el turno jugado o perdido

        if not self.__jail:  # Si no cayó en la carcel previamente juega el turno

            board_size = len(board)

            # ================ #
            #     Movement     #
            # ================ #
            self.movement(move, board_size)

            standing = board[self.position - 1]  # Propiedad sobre la cual ahora se encuentra situado el jugador

            # ================ #
            #    Behaviour     #
            # ================ #

            # Si pasa por la salida o parada libre no hace nada (El dinero se añade en la función turn)

            if standing.get_name() == 'GO' or standing.get_name() == 'Free Parking':
                pass  # Casilla libre
            elif standing.get_name() == 'Card':
                # No toma el valor del limite superior para generar los números
                action = np.random.randint(1, 4)
                # Se selecciona una valor a pagar o recibir de los disponibles
                amount = standing.get_amount()[np.random.randint(0, 6)]
                if action == 1:
                    self.pay(amount, board)  # Pago por la tarjeta
                elif action == 2:
                    self.earn(amount)  # Recibe dinero por la tarjeta
                else:
                    # Movimiento por tarjeta
                    move = np.random.randint(1, 4)  # Se elige de manera random cuantas casillas se va a mover [1,3]
                    self.turn(move, board, players, magic_card=True)

            elif standing.get_name() == 'Jail':
                self.jail()  # Si cae en la carce lo hace perder un turno
            else:

                if standing.get_owner() is None:  # Si la propiedad no tiene dueño
                    if self.compare(standing.get_value()):  # Si tiene dinero para comprarla
                        if np.random.rand(1) > 0.8:  # Decisión de compra
                            standing.set_owner(self.name)
                            self.pay(standing.get_value(), None, debt=False)  # Registro de dinero gastado
                            self.owned_props.append(standing)

                else:  # Si tiene dueño
                    # Busca el dueño y que no sea el mismo jugador
                    for player in players:
                        if standing.get_owner() == player.name and player.name != self.name:
                            self.pay(standing.get_fee(), board)  # Paga
                            player.earn(standing.get_fee())  # Registra las ganancias al jugador correspondiente

        # Si cayó en la carcel previamente solo se cambia el atributo para jugar el siguiente turno
        else:
            self.__jail = False


# Super clase celda, celdas o casillas donde no se realiza una acción
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


class Card(Cell):
    def __init__(self):
        self.__name = 'Card'
        self.__amount = [15, 20, 50, 100, 150, 200]
        super().__init__(self.__name)

    def get_amount(self):
        return self.__amount


class Property(Cell):
    def __init__(self, name, value, fee):
        self.__value = value  # Valor de la propiedad
        self.__fee = fee  # Valor de la renta
        self.__owner = None # Dueño de la propiedad
        super().__init__(name)

    def get_fee(self):
        return self.__fee

    def get_value(self):
        return self.__value

    def set_fee(self, amount, ):
        self.__fee = amount

    def get_owner(self):
        return self.__owner

    def set_owner(self, owner):
        """
        Set the owner of the property.
        :param owner:
        """
        self.__owner = owner
