import webapp2

from models.game import Game, create_game
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