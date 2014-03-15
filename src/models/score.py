from google.appengine.ext.ndb import model

import logging

class Score(model.Model):

    score = model.IntegerProperty(required=True)
    player_name = model.StringProperty(required=True)
    game_id = model.IntegerProperty(required=True)
    
    def change_score(self, score):
        
        self.score = score
        
        self.put()
    
    
def record_score(player_name, game_id, score):
        
    existing_score = get_score(player_name, game_id)    
    if existing_score:
        logging.error("Score already recorded for player %s in game %s.", player_name, game_id)  
        # TODO: Prompt for overwriting score  
        existing_score.change_score(score)
        
        return existing_score
        
    else:    
        new_score = Score()
        new_score.player_name = player_name
        new_score.game_id = game_id
        new_score.score = score
        
        new_score.put()
        
        return new_score
    
def get_score(player_name, game_id):
    
    scores = Score.query(Score.player_name == player_name, Score.game_id == game_id).fetch()
        
    return scores[0] if scores else None