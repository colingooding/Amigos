from google.appengine.ext.ndb import model

import logging
    
    
class Player(model.Model):

    name = model.StringProperty(required=True)


def create_player(name):
        
    if get_player(name):
        logging.error("Player named %s already exists! Use a unique name.", name)    
        return

    player = Player()
    player.name = name
    
    return player
    
def get_player(name):
    
    return Player.query(Player.name == name).fetch()