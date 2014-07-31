from google.appengine.ext.ndb import model
import json
import logging
    
class Course(model.Model):

    course_id = model.IntegerProperty(required=True)
    name = model.StringProperty(required=True)
    pars = model.JsonProperty(required=True)
        
    def get_par_for_hole(self, hole):
        
        pars = json.loads(self.pars)
        return pars.get(str(hole), None)
        
    def set_par_for_hole(self, hole, par):
        
        pars = json.loads(self.pars)
        pars[str(hole)] = par
        self.pars = json.dumps(pars)
        self.put()
        
    def set_name(self, name):
        
        self.name = name
        self.put()
        
    def get_length(self):
        
        pars = json.loads(self.pars)
        return len(pars)
        
        
def create_course(name, pars):
    
    if Course.query(Course.name == name).get():
        logging.error("Course named %s already exists! Use a unique name.", name)    
        return
    
    course = Course()
    course.course_id = Course.allocate_ids(1)[0]
    course.name = name
    course.pars = json.dumps(pars)
    
    course.put()
    
    return course
    
def get_course(course_id):
    
    return Course.query(Course.course_id == course_id).get()
        
        
    
    
    
    
