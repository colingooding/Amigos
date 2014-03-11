from webapp2 import Route

routes = [
    Route('/', handler='main.MainPage', name='main'),
    Route('/choose_players', handler='main.ChoosePlayers', name='choose_players'),
    Route('/new_player', handler='actions.players.NewPlayer', name='new_player'),
    ]