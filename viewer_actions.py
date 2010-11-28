from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import Key

from django.utils import simplejson

import models

class GetSongStats(webapp.RequestHandler):
  def post(self):
   #?key_name=sddf&key_name=dssfsd
   user = users.get_current_user()
   key_names = self.request.get_all('key_name')
   songs = models.ViewerSong.get_by_key_name(key_names, parent=get_viewer())
   song_dict = {}
   for song in songs:
     if song is not None:
       song_dict[song.key().name()] = song.json()
   self.response.out.write(simplejson.dumps(song_dict))
    
class UpdateSongStats(webapp.RequestHandler):
  def get(self):
    self.update_song()
    
  def post(self):
    self.update_song()
    
  def update_song(self):
    # Every request has &key_name=&title=&artist=
    # Then requests can have either &opinion= or &addview=
    viewer = get_viewer()
    
    key_name = self.request.get('key_name')
    song = models.ViewerSong.get_by_key_name(key_name, parent=viewer)
    if song is None:
      song = models.ViewerSong(key_name=key_name, parent=viewer)
      song.title = self.request.get('title')
      song.artist = self.request.get('artist')
      
    opinion = self.request.get('opinion')
    if opinion and opinion != song.opinion:
      old_opinion = song.opinion
      song.opinion = opinion
      self.update_global_song(key_name, song, opinion=True, old_opinion=old_opinion)
    if self.request.get('addview'):
      song.viewcount = song.viewcount + 1
      self.update_global_song(key_name, song, viewcount=True)
      
    song.put()
    self.response.out.write(simplejson.dumps(song.json()))
    
  def update_global_song(self, key_name, viewer_song, opinion=False, viewcount=False, old_opinion=None):
    global_song = models.Song.get_by_key_name(key_name)
    if global_song is None:
      global_song = models.Song(key_name=key_name)
      global_song.title = viewer_song.title
      global_song.artist = viewer_song.artist
    
    if opinion:
      # Need old opinion!
      if viewer_song.opinion == 'Yay':
        global_song.opinioncount_yay += 1
      elif viewer_song.opinion == 'Meh':
        global_song.opinioncount_meh += 1
      else:
        global_song.opinioncount_nay += 1
        
      if old_opinion:
        if old_opinion == 'Yay':
          global_song.opinioncount_yay -= 1
        elif old_opinion == 'Meh':
          global_song.opinioncount_meh -= 1
        else:
          global_song.opinioncount_nay -= 1
          
    elif viewcount:
      global_song.viewcount += 1
    
    global_song.put()
    
    
def get_viewer():
  user = users.get_current_user()
  # TODO: Do we have to retrieve this every time?
  viewer = models.Viewer.get_by_key_name(user.email())
  if viewer is None:
    viewer = models.Viewer(key_name=user.email())
    viewer.user = user
    viewer.put()
  return viewer