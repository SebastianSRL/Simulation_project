from entities import *


# Simula el lanzamiento de un dado
def throw_dice():
    """
    Simulates a dice
    :return: the result of throwing a dice
    """
    return np.random.randint(1, 6)


# Ordena los jugadores en orden de aquel que saca mayores valores en los dados
def sort_players(players):
    """
    Sort the players according
    :param players: list of players
    :return: sorted list of players according their results
    """
    result = np.zeros((len(players)))

    for i, _ in enumerate(players):
        result[i] = throw_dice()  # Almacena los resultados de cada lanzamiento de dados

    order = np.argsort(result, axis=0).astype(int)  # Da el nuevo ordenamiendo
    return [players[i] for i in order]  # Retorna la lista de jugadores en orden de lanzamiento


def main():
    money = 1500  # Dinero inicial para todos los jugadores
    bankrupt_players = []  # Almacenará los jugadores en bancarrota

    # Inicializa las propiedades
    board = [
        Cell('GO'),
        Property(name='Mediterranean Avenue', value=40, fee=2),
        Property(name='Baltic Avenue', value=60, fee=4),
        Property(name='Oriental Avenue', value=100, fee=6),
        Property(name='Vermont Avenue', value=100, fee=6),
        Property(name='Connecticut Avenue', value=100, fee=8),
        Jail(),
        Property(name='St. Charles place', value=120, fee=10),
        Property(name='States Avenue', value=140, fee=10),
        Property(name='Virginia Avenue', value=160, fee=12),
        Property(name='St James Place', value=180, fee=14),
        Property(name='Tennessee Avenue', value=180, fee=14),
        Property(name='New York Avenue', value=200, fee=16),
        Property(name='Kentucky Avenue', value=220, fee=18),
        Property(name='Indiana Avenue', value=220, fee=18),
        Property(name='Illinois Avenue', value=240, fee=20),
        Property(name='Atlantic Avenue', value=260, fee=22),
        Property(name='Ventnor Avenue', value=260, fee=22),
        Property(name='Marvin Gardens', value=280, fee=24),
        Jail(),
        Property(name='Pacific Avenue', value=300, fee=26),
        Property(name='North Carolina Avenue', value=300, fee=26),
        Property(name='Pennsilvania Avenue', value=320, fee=28),
        Property(name='Park Place', value=350, fee=35),
        Property(name='Boardwalk', value=400, fee=50)
    ]

    # Inicializa los jugadores junto con su dinero
    players = [
        Player("Juan", money),
        Player("Sebastian", money),
        Player("Geison", money),
        Player("Paula", money)
    ]

    # Ordena el los jugadores e imprime el orden
    players = sort_players(players)
    print(f"Orden de lanzamiento de dados: {[player.name for player in players]}\n")

    while len(players) >= 2:  # Mientras haya al menos dos jugadores en juego

        for i, player in enumerate(players):  # Hace que todos los jugadores activos jueguen
            if len(players) >= 2:  # Antes de jugar el siguiente turno verfica si hay al menos dos jugadores activos
                if player.bankruptcy():  # Si un jugador entra en bancarrota los saca de los jugadores activos y lo mete en los de bancarrota
                    bankrupt_players.append(player)
                    players.pop(i)
                else:
                    movement = throw_dice() + throw_dice()  # Lanzamiendo de los dados
                    player.turn(movement, board, players)  # Juega el turno de un jugador
            else:
                break

    # Imprime un resumen del juego
    print(f" !!!! El ganador fue: {players[0].name} con ${players[0].money} !!!! \n")
    print(f"""Resumen del juego:\n
    {players[0].name} gastó: {players[0].spend * -1} y ganó: {players[0].earned}  jugando {players[0].turn_counter} turnos y {players[0].go_counter} vueltas al tablero
    {bankrupt_players[2].name} gastó: {bankrupt_players[2].spend * -1} y ganó: {bankrupt_players[2].earned} jugando {bankrupt_players[2].turn_counter} turnos y {bankrupt_players[2].go_counter} vueltas al tablero
    {bankrupt_players[1].name} gastó: {bankrupt_players[1].spend * -1} y ganó: {bankrupt_players[1].earned} jugando {bankrupt_players[1].turn_counter} turnos y {bankrupt_players[1].go_counter} vueltas al tablero
    {bankrupt_players[0].name} gastó: {bankrupt_players[0].spend * -1} y ganó: {bankrupt_players[0].earned} jugando {bankrupt_players[0].turn_counter} turnos y {bankrupt_players[0].go_counter} vueltas al tablero

    """)
    return -1


if __name__ == '__main__':
    main()
