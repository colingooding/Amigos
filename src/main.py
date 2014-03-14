import os

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

application = webapp2.WSGIApplication(routes=routes, debug=True)
