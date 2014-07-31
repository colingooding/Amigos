from google.appengine.ext.ndb import model

import json

class Score(model.Model):

    score = model.IntegerProperty()
    player_name = model.StringProperty(required=True)
    game_id = model.IntegerProperty(required=True)
    hole_scores = model.JsonProperty()
    
    def get_score_for_hole(self, hole):
        
        scores = json.loads(self.hole_scores)
        return scores.get(hole, None)
        
    def record_score_for_hole(self, hole, score):
        
        scores = {}
        if self.hole_scores:
            scores = json.loads(self.hole_scores)
        scores[hole] = score
        self.hole_scores = json.dumps(scores)
        self.put()
        
    def record_final_score(self, score):
        
        self.score = score
        self.put()
    
    def calculate_final_score(self):
        
        final_score = 0
        scores = json.loads(self.hole_scores)
        for hole, hole_score in scores.iteritems():
            final_score += hole_score
        self.record_final_score(final_score)
    
def get_score(player_name, game_id):
    
    return Score.query(Score.player_name == player_name, Score.game_id == game_id).get()