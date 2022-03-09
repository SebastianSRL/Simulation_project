import time

from entities import *


# Ordena los jugadores en orden de aquel que saca mayores valores en los dados
def sort_players(players):
    """
    Sort the players according
    :param players: list of players
    :return: sorted list of players according their results
    """
    result = np.zeros((len(players)))

    for i, player in enumerate(players):
        result[i] = player.throw_dice()  # Almacena los resultados de cada lanzamiento de dados

    order = np.argsort(result, axis=0).astype(int)[::-1]  # Da el nuevo ordenamiendo
    return [players[i] for i in order]  # Retorna la lista de jugadores en orden de lanzamiento


def initialize_game(money=1500):
    # Inicializa las propiedades
    board = [
        Cell('GO'),
        Property(name='Mediterranean Avenue', value=40, fee=2),
        Card(),
        Property(name='Baltic Avenue', value=60, fee=4),
        Property(name='Oriental Avenue', value=100, fee=6),
        Card(),
        Property(name='Vermont Avenue', value=100, fee=6),
        Property(name='Connecticut Avenue', value=100, fee=8),
        Jail(),
        Property(name='St. Charles place', value=120, fee=10),
        Card(),
        Property(name='States Avenue', value=140, fee=10),
        Property(name='Virginia Avenue', value=160, fee=12),
        Property(name='St James Place', value=180, fee=14),
        Card(),
        Property(name='Tennessee Avenue', value=180, fee=14),
        Property(name='New York Avenue', value=200, fee=16),
        Cell('Free Parking'),
        Property(name='Kentucky Avenue', value=220, fee=18),
        Card(),
        Property(name='Indiana Avenue', value=220, fee=18),
        Property(name='Illinois Avenue', value=240, fee=20),
        Property(name='Atlantic Avenue', value=260, fee=22),
        Property(name='Ventnor Avenue', value=260, fee=22),
        Card(),
        Property(name='Marvin Gardens', value=280, fee=24),
        Jail(),
        Property(name='Pacific Avenue', value=300, fee=26),
        Property(name='North Carolina Avenue', value=300, fee=26),
        Card(),
        Property(name='Pennsilvania Avenue', value=320, fee=28),
        Card(),
        Property(name='Park Place', value=350, fee=35),
        Property(name='Boardwalk', value=400, fee=50)
    ]

    # Inicializa los jugadores junto con su dinero
    players = [
        # Player("Juan", money),
        Player("Sebastian", money),
        Player("Geison", money),
        Player("Paula", money),
        Player("María", money),
    ]

    return board, players


# Revisar Lógica
def play(board, players, summary=True):
    active_players = np.ones((len(players)))
    bankrupt_players = []
    counter = 1
    if summary:
        print(f"Orden de lanzamiento de dados: {[player.name for player in players]}\n")

    while len(players) >= 2:  # Mientras haya al menos dos jugadores en juego

        for player in players:  # Hace que todos los jugadores activos jueguen
            movement = player.throw_dice() + player.throw_dice()  # Lanzamiendo de los dados
            player.turn(movement, board, players)  # Juega el turno de un jugador

            if counter % 100 == 0:
                for prop in board:
                    if prop.get_name() not in ['GO', 'Card', 'Free Parking', 'Jail']:
                        prop.set_fee(prop.get_fee() * 2.0)

            if len(players) == 2 and player.bankruptcy():
                break
            counter += 1
        # counter += 1

        for player in players:
            # Si un jugador entra en bancarrota los saca de los jugadores activos y lo mete en la lista de bancarrota
            if player.bankruptcy():
                bankrupt_players.append(player)
                players.remove(player)

    # Imprime un resumen del juego
    if summary:
        print(f" !!!! El ganador fue: {players[0].name} con ${players[0].money} !!!! \n")
        print(
            f"Resumen del juego:\n{players[0].name} gastó: {players[0].spend * -1} y ganó: {players[0].earned}  jugando {players[0].turn_counter} turnos y {players[0].go_counter} vueltas al tablero")
        for bankrupt_player in reversed(bankrupt_players):
            print(
                f"{bankrupt_player.name} gastó: {bankrupt_player.spend * -1} y ganó: {bankrupt_player.earned} quedando con una deuda de {bankrupt_player.debt} jugando {bankrupt_player.turn_counter} turnos y {bankrupt_player.go_counter} vueltas al tablero")

    return players, bankrupt_players


def main():

    trials = 1000
    for _ in range(trials):
        # Dinero inicial para todos los jugadores
        money = 1500
        board, players = initialize_game(money)

        # Ordena el los jugadores e imprime el orden
        players = sort_players(players)

        # Se juega la partida de Monopoly y se retorna los jugadores con sus estadisticas
        players, bankrupt_players = play(board, players, summary=False)

    return -1


if __name__ == '__main__':
    t = time.time()
    main()
    print(f"Execution time: {time.time() - t:.5f}[s]")
