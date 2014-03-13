from models.score import Score
from models.game import Game

import copy

def calculate_owings_for_game(game_id):
    
    scores = Score.query(Score.game_id == game_id).fetch()
    
    owings = {}
    for score in scores:
        
        owings[score.player_name] = {} 
        
    while scores:
        
        score_one = scores.pop()
        
        for score_two in scores:
        
            amount = score_one.score - score_two.score
            
            if amount > 0:
                
                owings[score_two.player_name].update({score_one.player_name :  amount})
                
            elif amount < 0:
            
                owings[score_one.player_name].update({score_two.player_name : - amount})
                
            
    return owings

def calculate_payments_from_owings(owings, game_id):
    
    game = Game.query(Game.game_id == game_id).fetch()[0]
    
    max_payment = game.max_payment / game.point_value
    
    for player_paying_name, value in owings.iteritems():
        
        owings_for_paying_player = copy.deepcopy(value)
        
        total_payment = 0
    
        max_reached = False
        
        for _ in range(len(owings_for_paying_player)):
        
            player_receiving_name = max(owings_for_paying_player, key=owings_for_paying_player.get)
            
            paying_amount = owings_for_paying_player.pop(player_receiving_name)
            
            if max_reached:
                
                owings[player_paying_name].pop(player_receiving_name)
            
            else:    
                
                total_payment += paying_amount
                
                excess = total_payment - max_payment
                
                if excess > 0:
                    
                    max_reached = True
                    
                    paying_amount -= excess
    
                owings_for_receiving_player = copy.deepcopy(owings[player_receiving_name])
                    
                while owings_for_receiving_player:
                    
                    indirect_player_receiving_name = max(owings_for_receiving_player, key=owings_for_receiving_player.get)
                
                    indirect_paying_amount = owings_for_receiving_player.pop(indirect_player_receiving_name)
                    
                    still_owing = paying_amount - indirect_paying_amount
                    
                    if still_owing <= 0:
                        
                        if still_owing == 0:
                        
                            owings[player_receiving_name].pop(indirect_player_receiving_name)
                        
                        else:
                            
                            owings[player_receiving_name][indirect_player_receiving_name] = - still_owing
                        
                        owings[player_paying_name][indirect_player_receiving_name] += paying_amount
                        
                        owings[player_paying_name].pop(player_receiving_name)
                        
                        break
                    
                    else:
                        
                        owings[player_receiving_name].pop(indirect_player_receiving_name)
                        
                        owings[player_paying_name][indirect_player_receiving_name] += indirect_paying_amount
                        
                        owings[player_paying_name][player_receiving_name] = still_owing
                        
                        paying_amount = still_owing
                        
    return owings
            
                