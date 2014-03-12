from google.appengine.ext.ndb import model

from models.score import Score 

import logging

class Debt(model.Model):

    game_id = model.IntegerProperty(required=True)
    player_paying_name = model.StringProperty(required=True)
    player_receiving_name = model.StringProperty(required=True)
    amount = model.IntegerProperty(required=True)
        
def record_debt(game_id, score_one, score_two):
        
    existing_debt = get_debt(game_id, score_one.player_name, score_two.player_name)    
    if existing_debt:
        logging.error("debt already recorded for players %s and %s in game %s.", score_one.player_name, score_two.player_name, game_id)  
        return
    else:    
        new_debt = Debt()
        new_debt.game_id = game_id
        
        amount = score_one.score - score_two.score
        
        if amount > 0:
        
            new_debt.player_paying_name = score_two.player_name
            new_debt.player_receiving_name = score_one.player_name
            new_debt.amount = amount
            
        elif amount < 0:
        
            new_debt.player_paying_name = score_one.player_name
            new_debt.player_receiving_name = score_two.player_name
            new_debt.amount = - amount
            
        return new_debt
    
def get_debt(game_id, player_paying_name, player_receiving_name):
    
    return Debt.query(Debt.game_id == game_id,
                            Debt.player_paying_name == player_paying_name,
                            Debt.player_receiving_name == player_receiving_name).fetch()
    
def record_debts_for_game(game_id):
    
    scores = Score.query(Score.game_id == game_id).fetch()
    
    for score_one in scores:
        
        for score_two in scores:
            
            if score_one != score_two:
                
                record_debt(game_id, score_one, score_two)