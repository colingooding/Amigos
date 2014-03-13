from google.appengine.ext.ndb import model

import logging
    
    
class Game(model.Model):

    game_id = model.IntegerProperty(required=True)
    max_payment = model.FloatProperty(required=True)
    point_value = model.FloatProperty(required=True)

def create_game(game_id, max_payment=None, point_value=None):
        
    if get_game(game_id):
        logging.error("Game with id %s already exists! ", game_id)    
        return
    else:    
        game = Game()
        game.game_id = game_id
        game.max_payment = max_payment or 10.00
        game.point_value = point_value or 0.05
        
        game.put()
    
def get_game(game_id):
    
    return Game.query(Game.game_id == game_id).fetch()