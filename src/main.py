import os

from models.player import Player 

import jinja2
import webapp2

from urls import routes


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    
    
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())
        
class ChoosePlayers(webapp2.RequestHandler):
    
    
    def get(self):
        
        players = Player.query().fetch()
        context = {
            'players': players,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/choose_players.html')
        self.response.write(template.render())


#application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
#choose = webapp2.WSGIApplication([('/choose_players', ChoosePlayers)], debug=True)
application = webapp2.WSGIApplication(routes=routes, debug=True)
