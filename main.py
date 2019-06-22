
mode = ''
while mode != 'l' and mode != 'n':
    mode = input('[l] Local ou [n] Network?\n');


### CREATE PLAYERS ###
if mode == 'l':
    import game

    g = game.Game()

    g.p1 = g.newPlayer(1, g.ships[:], g.p1Field, g.p1BombField)
    input('Aperta enter, vacilão')
    g.clear()
    
    g.p2 = g.newPlayer(2, g.ships[:], g.p2Field, g.p2BombField)
    input('Enter man...')
    g.clear()

    g.start()
else:
    sc = ''
    while sc != 's' and sc != 'c':
        sc = input('[s] Server ou [c] Cliente?\n');
    if sc == 's':
        import server
        s = server.Server()
        s.connect()

    else:
        import client
        
        c = client.Client()