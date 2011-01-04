from datetime import datetime
import time
import re

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue
from google.appengine.ext import deferred
from google.appengine.api import users
from google.appengine.ext.db import Key

class ViewerSong(db.Model):
  # parent key is a made up key of User and email
  opinion = db.StringProperty()
  viewcount = db.IntegerProperty(default=0)
  title = db.StringProperty()
  artist = db.StringProperty()
  viewer = db.UserProperty(auto_current_user_add=True)
  
  def json(self):
    return {'opinion': self.opinion,
            'viewcount': self.viewcount,
            'title': self.title,
            'artist': self.artist}
            
  @classmethod
  def get_by_key_name_for_viewer(cls, key_names):  
    parent_key = Key.from_path('User', users.get_current_user().email())
    return cls.get_by_key_name(key_names, parent=parent_key)
     
  @classmethod
  def make_with_key_name_for_viewer(cls, key_name):
    parent_key = Key.from_path('User', users.get_current_user().email())
    return cls(key_name=key_name, parent=parent_key)
     
class Song(db.Model):
  # keyname
  # no parentkey
  opinioncount_nay = db.IntegerProperty(default=0)
  opinioncount_meh = db.IntegerProperty(default=0)
  opinioncount_yay = db.IntegerProperty(default=0)
  viewcount = db.IntegerProperty(default=0)
  title = db.StringProperty()
  artist = db.StringProperty()
  
  
  def json(self):
    return {'opinioncount_nay': self.opinioncount_nay,
            'opinioncount_meh': self.opinioncount_meh,
            'opinioncount_yay': self.opinioncount_yay,
            'viewcount': self.get_viewcount(),
            'title': self.title,
            'artist': self.artist}
            
  def get_viewcount(self):
    viewcount = self.viewcount
    cached_viewcount = memcache.get('viewcount-' + self.key().name(), self.key().kind())
    if cached_viewcount:
      viewcount += cached_viewcount
    return viewcount

  @classmethod
  def flush_viewcount(cls, name):
    song = cls.get_by_key_name(name)
    if not song:
      song = cls()

    # Get the current value
    value = memcache.get('viewcount-' + name, cls.kind())

    # Subtract it from the memcached value
    if not value:
      return
      
    memcache.decr('viewcount-' + name, value, cls.kind())

    # Store it to the counter
    song.viewcount += value
    song.put()
    
  @classmethod
  def incr_viewcount(cls, name, interval=5, value=1):
    """Increments the named counter.

    Args:
      name: The name of the counter.
      interval: How frequently to flush the counter to disk.
      value: The value to increment by.
    """
    memcache.incr('viewcount-' + name, value, cls.kind())
    interval_num = get_interval_number(datetime.now(), interval)
    task_name = '-'.join([cls.kind(), re.sub('[^a-zA-Z0-9-]*', '', name), 'viewcount', str(interval), str(interval_num)])
    try:
      deferred.defer(cls.flush_viewcount, name, _name=task_name)
    except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError):
      pass
    
def get_interval_number(ts, duration):
  """Returns the number of the current interval.

  Args:
    ts: The timestamp to convert
    duration: The length of the interval
  Returns:
    int: Interval number.
  """
  return int(time.mktime(ts.timetuple()) / duration)