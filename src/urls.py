from webapp2 import Route

routes = [
    Route('/', handler='main.MainPage', name='main'),
    Route('/choose_players', handler='actions.players.ChoosePlayers', name='choose_players'),
    Route('/new_player', handler='actions.players.NewPlayer', name='new_player'),
    Route('/load_games', handler='actions.games.LoadGames', name='load_games'),
    Route('/start_game', handler='actions.games.StartGame', name='start_game'),
    Route('/enter_scores', handler='actions.scores.EnterScores', name='enter_scores'),
    Route('/calculate_scores', handler='actions.scores.CalculateScores', name='calculate_scores'),
    ]