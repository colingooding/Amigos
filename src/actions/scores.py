
import webapp2

from models.score import Score, record_score 
from models.player import Player
from models.debt import Debt


def calculate_owings_for_game(game_id):
    
    debts = Debt.query(Debt.game_id == game_id).fetch()
    
    owings = {}
        
    for debt in debts:
        
        if owings[debt.player_paying_name]:
            
            owings[debt.player_paying_name].update({debt.player_receiving_name :  debt.amount})
            
        else:
            
            owings[debt.player_paying_name] = {debt.player_receiving_name :  debt.amount}
            
    return owings
