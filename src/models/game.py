from google.appengine.ext.ndb import model

import logging
import datetime
    
class Game(model.Model):

    game_id = model.IntegerProperty(required=True)
    max_payment = model.FloatProperty(required=True)
    point_value = model.FloatProperty(required=True)
    created = model.DateTimeProperty(required=True)
    player_list = model.StringProperty()
        

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

def add_player_to_game(player, game_id):
        
    game = get_game(game_id)
    
    if game.player_list == None:
        
        game.player_list = player
        print "test1"
        
    else:
        
        game.player_list = game.player_list + ", " + player
        print "test2"
        
    game.put()
        
def get_players_in_game(game_id):
    
    game = get_game(game_id)
    
    players = game.player_list.split(", ")
    
    return players
    
    
    
