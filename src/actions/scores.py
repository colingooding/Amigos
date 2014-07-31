from models.score import Score, get_score
from models.game import get_game
from models.course import get_course

import webapp2
import copy
import json
import logging

from main import JINJA_ENVIRONMENT
    
def calculate_owings(scores, game):
        
    owings = {}
    
    for score in scores:
        
        owings[score.player_name] = {} 
        
    while scores:
        
        score_one = scores.pop()
        
        for score_two in scores:
        
            amount = score_one.score  - score_two.score
            amount = amount * game.point_value 
            
            if amount > 0:
                
                owings[score_one.player_name].update({score_two.player_name :  amount})
                
            elif amount < 0:
            
                owings[score_two.player_name].update({score_one.player_name : - amount})
                
            
    return owings

def calculate_payments_from_owings(owings, game):

    max_payment = game.max_payment
    
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
                
                if owings_for_receiving_player:
                        
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
                    
                else:
                        
                    owings[player_paying_name][player_receiving_name] = paying_amount
                        
    return owings

class EnterFinalScores(webapp2.RequestHandler):
    
    
    def get(self):
        
        game_id = self.request.get('game_id')
        game = get_game(int(game_id))
        
        players = game.get_players()
        
        players_in_game = None
        if players:
            players_in_game = ', '.join(players)
        
        context = {
            'game_id': game_id,
            'players': players,
            'players_in_game': players_in_game,
            'jplayers': json.dumps(players),
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/enter_final_scores.html')
        self.response.write(template.render(context))
        

class CalculatePayments(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        load_game = self.request.get('load_game')
        
        jplayers = self.request.get('jplayers')
        
        logging.info("jplayers id is |%s|", jplayers)
        
        players = json.loads(jplayers) if jplayers != 'None' else []
            
        scores = []
        
        if load_game == "true":
            scores = Score.query(Score.game_id == game_id).fetch()
        else:
            for player in players:
                score = Score(player_name=player, game_id=game_id, score=int(self.request.get(player)))
                score.put()
                scores.append(score)
            
        game = get_game(int(game_id))
        
        owings = calculate_owings(scores, game)
        
        payments = calculate_payments_from_owings(owings, game)
        
        context = {
            'game_id': game_id,
            'scores': scores,
            'players': players,
            'payments': payments
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/payments.html')
        self.response.write(template.render(context))
        

class EnterScoresForHole(webapp2.RequestHandler):
    
    
    def get(self):
        
        game_id = self.request.get('game_id')
        hole = self.request.get('hole')
        game = get_game(int(game_id))
        
        course = get_course(game.course_id)
        
        players = game.get_players()
        
        players_in_game = None
        if players:
            players_in_game = ', '.join(players)
        
        context = {
            'game_id': game_id,
            'hole': hole,
            'players': players,
            'players_in_game': players_in_game,
            'jplayers': json.dumps(players),
            'course': course.name,
            'par': course.get_par_for_hole(hole)
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/enter_hole_scores.html')
        self.response.write(template.render(context))
        

class SubmitScoresForHole(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        load_game = self.request.get('load_game')
        hole = int(self.request.get('hole'))
        
        #TODO: Load scores
        
        next_hole = hole + 1
        
        jplayers = self.request.get('jplayers')
        logging.info("jplayers id is |%s|", jplayers)
        
        players = json.loads(jplayers) if jplayers != 'None' else []
        
        game = get_game(int(game_id))
        course = get_course(game.course_id)
        
        par = course.get_par_for_hole(str(hole))
        
        left_team = {'players': [], 'scores': [], 'flip': False}
        right_team = {'players': [], 'scores': [], 'flip': False}
        for player in players:
            score = int(self.request.get(player))
            flip = False
            if score < par:
                flip = True
                
            if self.request.get("%s-left" % player):
                left_team['players'].append(player)
                left_team['scores'].append(score)
                if flip:
                    left_team['flip'] = flip
            else:
                right_team['players'].append(player)
                right_team['scores'].append(score)
                if flip:
                    right_team['flip'] = flip
                    
        left_score = get_score_for_team(left_team, right_team.get('flip'))
        right_score = get_score_for_team(right_team, left_team.get('flip'))
            
            
                
        scores = []
        for player in left_team.get('players'):
            score = record_and_retrieve_score_for_hole(player, game_id, hole, left_score)
            scores.append(score)
            
        for player in right_team.get('players'):
            score = record_and_retrieve_score_for_hole(player, game_id, hole, right_score)
            scores.append(score)
        
        context = {
            'game_id': game_id,
            'players': players,
        }
            
        
        if course.get_length() < next_hole:
            #game is complete
            for score in scores:
                score.calculate_final_score()
            
            owings = calculate_owings(scores, game)
            
            payments = calculate_payments_from_owings(owings, game)
            
            context.update({'payments': payments})
            
            template = JINJA_ENVIRONMENT.get_template('templates/payments.html')
            self.response.write(template.render(context))
            
        else:
        
            players_in_game = None
            if players:
                players_in_game = ', '.join(players)
                
            course = get_course(game.course_id)
            
            context.update({
                'hole': next_hole,
                'players_in_game': players_in_game,
                'jplayers': json.dumps(players),
                'course': course.name,
                'par': course.get_par_for_hole(next_hole)
            })
            template = JINJA_ENVIRONMENT.get_template('templates/enter_hole_scores.html')
            self.response.write(template.render(context))
            
def record_and_retrieve_score_for_hole(player, game_id, hole, team_score):
    score = get_score(player, game_id)
    if not score:
        score = Score(player_name=player, game_id=game_id)
    score.record_score_for_hole(hole, team_score)
    return score
            
def get_score_for_team(team, flip):                
    score_1 = team.get('scores')[0]
    score_2 = team.get('scores')[1]
    
    if score_1 < score_2:
        return calculate_score_for_teammates(score_1, score_2, flip)
    else:
        return calculate_score_for_teammates(score_2, score_1, flip)
        
def calculate_score_for_teammates(score_1, score_2, flip):
    if not flip: 
        return (score_1 * 10) + score_2
    else: 
        return (score_2 * 10) + score_1
    
                