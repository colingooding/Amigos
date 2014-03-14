
import webapp2

from models.player import create_player, Player
from models.game import add_player_to_game
from main import JINJA_ENVIRONMENT


class NewPlayer(webapp2.RequestHandler):
    
    def post(self):
        
        player = create_player(self.request.get('name'))
        if not player:
            raise StandardError('A player with that name already exists. You must use a unique name.')
        player.put()
        
        context = {
            'name': player.name,
            'game_id': self.request.get('game_id')
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/player_added.html')
        self.response.write(template.render(context))
        
class ChoosePlayers(webapp2.RequestHandler):
    
    
    def get(self):
        
        game_id = self.request.get('game_id')
        player_added_to_game = self.request.get('player_added_to_game')
        
        if player_added_to_game:
            
            add_player_to_game(player_added_to_game, int(game_id))
        
        players = Player.query().fetch()
        context = {
            'players': players,
            'game_id': game_id,
            'player_added_to_game': self.request.get('player_added_to_game'),
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render(context))