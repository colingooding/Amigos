from google.appengine.ext.ndb import model

import logging


def create_player(name):
        
    if get_player(name):
        logging.error("Player named %s already exists! Use a unique name.", name)    
        return
    else:    
        player = Player()
        player.name = name
        
        return player
    
def get_player(name):
    
    return Player.query(Player.name == name).fetch()
    
    
def player_score(name, score):
        
    player = Player()
    player.name = name
    
    return player
    
class Player(model.Model):
    """ Partner class """

    name = model.StringProperty(required=True)
    score = model.FloatProperty()