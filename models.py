from google.appengine.ext import db


class Viewer(db.Model):
  # key is email
  user = db.UserProperty()
  
class ViewerSong(db.Model):
  # keyname
  # parent key is a viewer
  opinion = db.StringProperty()
  viewcount = db.IntegerProperty(default=0)
  title = db.StringProperty()
  artist = db.StringProperty()
  
  def json(self):
    return {'opinion': self.opinion,
            'viewcount': self.viewcount,
            'title': self.title,
            'artist': self.artist}
            
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
            'viewcount': self.viewcount,
            'title': self.title,
            'artist': self.artist}