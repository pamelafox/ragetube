import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

    
class BasePage(webapp.RequestHandler):
  """The base class for actual pages to subclass."""

  def get(self):
    self.render(self.get_template_filename(), self.get_template_values())

  def get_template_values(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      loggedin = 'true'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'
      loggedin = 'false'

    template_values = {
      'loggedin': loggedin,
      'url': url,
      'url_linktext': url_linktext,
    }
    return template_values

  def get_template_filename(self):
    return 'base.html'

  def render(self, filename, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    self.response.out.write(template.render(path, template_values))
	
	
class Player(BasePage):
  def get_template_filename(self):
    return 'player.html'

class Stats(BasePage):
  def get_template_filename(self):
    return 'stats.html'
    