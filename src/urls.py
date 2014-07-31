from webapp2 import Route

routes = [
    Route('/', handler='main.MainPage', name='home'),
    Route('/choose_players', handler='actions.players.ChoosePlayers', name='choose_players'),
    Route('/new_player', handler='actions.players.NewPlayer', name='new_player'),
    Route('/load_games', handler='actions.games.LoadGames', name='load_games'),
    Route('/start_game', handler='actions.games.StartGame', name='start_game'),
    Route('/enter_final_scores', handler='actions.scores.EnterFinalScores', name='enter_final_scores'),
    Route('/enter_scores_for_hole', handler='actions.scores.EnterScoresForHole', name='enter_scores_for_hole'),
    Route('/payments', handler='actions.scores.CalculatePayments', name='calculate_payments'),
    Route('/submit_scores', handler='actions.scores.SubmitScoresForHole', name='submit_scores_for_hole'),
    Route('/edit_game', handler='actions.games.EditGame', name='edit_game'),
    Route('/submit_edited_game', handler='actions.games.SubmitEditedGame', name='submit_edited_game'),
    Route('/edit_course', handler='actions.courses.EditCourse', name='edit_course'),
    Route('/submit_edited_course', handler='actions.courses.SubmitEditedCourse', name='submit_edited_course'),
    Route('/choose_course', handler='actions.courses.ChooseCourse', name='choose_course'),
    Route('/submit_chosen_course', handler='actions.courses.SubmitChosenCourse', name='submit_chosen_course'),
    ]