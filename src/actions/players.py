
import webapp2

from models.player import create_player 

class NewPlayer(webapp2.RequestHandler):
    
    def post(self):
        
        player = create_player(self.request.get('name'))
        if not player:
            raise StandardError('A player with that name already exists. You must use a unique name.')
        player.put()
        
