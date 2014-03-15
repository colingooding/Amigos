import webapp2

from models.game import Game, create_game, get_game
from models.player import Player
from main import JINJA_ENVIRONMENT
        
class LoadGames(webapp2.RequestHandler):
    
    
    def get(self):
        
        games = Game.query().fetch()
        context = {
            'games': games,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/load_games.html')
        self.response.write(template.render(context))
        
        
class StartGame(webapp2.RequestHandler):
    
    
    def get(self):
        
        game = create_game()
        
        players = Player.query().fetch()
        context = {
            'players': players,
            'game_id': game.game_id
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render(context))
    
    
class EditGame(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        game = get_game(game_id)
        
        
        context = {
            'game_id': game_id,
            'players_in_game': self.request.get('players_in_game'),
            'max_payment': game.max_payment,
            'point_value': game.point_value
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/edit_game.html')
        self.response.write(template.render(context))

class SubmitEditedGame(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        game = get_game(game_id)
        
        max_payment = float(self.request.get('max_payment') or game.max_payment)
        point_value = float(self.request.get('point_value') or game.point_value)

        game.edit_game(max_payment, point_value)
        
        players = Player.query().fetch()
        
        context = {
            'game_id': game_id,
            'players': players,
            'players_in_game': self.request.get('players_in_game'),
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render(context))
        
        #self.redirect(webapp2.uri_for('choose_players'))
        
        