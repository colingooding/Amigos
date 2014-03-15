
import webapp2

from models.player import create_player, Player
from models.game import get_game, player_is_in_game
from main import JINJA_ENVIRONMENT


class NewPlayer(webapp2.RequestHandler):
    
    def post(self):
        
        name = self.request.get('name')
        player = create_player(name)
        
        error = None
        if not player:
            if name:
                error = "already exists. You must use a unique name."
            else:
                error = "You didn't enter a name!"
        else:
            name = player.name
            player.put()
        
        context = {
            'name': name,
            'game_id': self.request.get('game_id'),
            'error': error,
            'players_in_game': self.request.get('players_in_game'),
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/player_added.html')
        self.response.write(template.render(context))
        
class ChoosePlayers(webapp2.RequestHandler):
    
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        
        player_added_to_game = self.request.get('player_added_to_game')
        
        players_in_game = self.request.get('players_in_game')
        
        player_exists = False
        
        if player_added_to_game:
            game = get_game(game_id)
            
            if player_is_in_game(game, player_added_to_game):
                player_exists = player_added_to_game
            else:
                game.add_player(player_added_to_game)
        
                if players_in_game:
                    players_in_game += ", " + player_added_to_game
                else:
                    players_in_game = player_added_to_game
        
        players = Player.query().fetch()
        context = {
            'players': players,
            'game_id': game_id,
            'players_in_game': players_in_game,
            'player_exists': player_exists
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render(context))