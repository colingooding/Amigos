from google.appengine.ext.ndb import model

import datetime
import json
    
class Game(model.Model):

    game_id = model.IntegerProperty(required=True)
    max_payment = model.FloatProperty(required=True)
    point_value = model.FloatProperty(required=True)
    created = model.DateTimeProperty(required=True)
    player_list = model.JsonProperty()
        
    def get_players(self):
        
        if self.player_list:
            
            return json.loads(self.player_list)
        
        else:
            
            return None
    
    def add_player(self, player):
        
        if self.player_list == None:
            
            self.player_list = json.dumps([player])
            
        else:
            
            players = json.loads(self.player_list)
            
            players.append(player)
            
            self.player_list = json.dumps(players)
            
        self.put()
        
    def readable_players(self):
        
        players = self.get_players()
        
        return ', '.join(players)
        
        
def create_game(max_payment=None, point_value=None):
        
    game_id = Game.allocate_ids(1)[0]  
    
    game = Game()
    game.game_id = game_id
    game.max_payment = max_payment or 10.00
    game.point_value = point_value or 0.05
    game.created = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    
    game.put()
    
    return game
    
def get_game(game_id):
    
    return Game.query(Game.game_id == game_id).fetch()[0]

def player_is_in_game(game, player):
    
    players = game.get_players()
    
    if not players:
        return False
    else:
        return True if player in players else False
        
        
    
    
    
    
