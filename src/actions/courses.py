import webapp2
import json

from models.course import Course, create_course, get_course
from models.player import Player
from models.game import get_game
from main import JINJA_ENVIRONMENT
    
    
class EditCourse(webapp2.RequestHandler):
    
    def get(self):
        
        context = {
            'game_id': self.request.get('game_id'),
            'players_in_game': self.request.get('players_in_game'),
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/edit_course.html')
        self.response.write(template.render(context))
    
class SubmitEditedCourse(webapp2.RequestHandler):
    
    def post(self):

        pars = self.request.get('pars')
        
        par_list = [x.strip() for x in pars.split(',')]
        
        pars = {}
        for x in range(0,len(par_list)):
            pars[str(x+1)] = int(par_list[x])
        
        create_course(self.request.get('course_name'), pars)
        
        players = Player.query().fetch()
        
        context = {
            'game_id': self.request.get('game_id'),
            'players_in_game': self.request.get('players_in_game'),
            'players': players,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render(context))
        
        
class ChooseCourse(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        
        courses = Course.query().fetch()
        
        context = {
            'game_id': game_id,
            'courses': courses,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_course.html')
        self.response.write(template.render(context))
        
class SubmitChosenCourse(webapp2.RequestHandler):
    
    def get(self):
        
        game_id = int(self.request.get('game_id'))
        course_id = int(self.request.get('course_id'))
        
        game = get_game(game_id)
        
        players = game.get_players()
        
        players_in_game = None
        if players:
            players_in_game = ', '.join(players)

        game = get_game(game_id)
        
        game.course_id = course_id
        game.put()
            
        course = get_course(course_id)
        hole = 1
        
        context = {
            'hole': hole,
            'game_id': game_id,
            'players': players,
            'players_in_game': players_in_game,
            'jplayers': json.dumps(players),
            'course': course.name,
            'par': course.get_par_for_hole(hole)
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/enter_hole_scores.html')
        self.response.write(template.render(context))