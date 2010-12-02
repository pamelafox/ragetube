import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

from django.utils import simplejson

import models

class GetSongStats(webapp.RequestHandler):

  def post(self):
    # accept multiple song keys
    # return json
    key_names = self.request.get_all('key_name')
    songs = models.Song.get_by_key_name(key_names)
    song_dict = {}
    for song in songs:
      if song is not None:
        song_dict[song.key().name()] = song.json()
    self.response.out.write(simplejson.dumps(song_dict))
  
class GetTopSongs(webapp.RequestHandler):

  def get(self):
    self.get_top_songs()
    
  def post(self):
    self.get_top_songs()
  
  def get_top_songs(self):
    most_viewed = models.Song.all().order('-viewcount').get()
    most_yayed = models.Song.all().order('-opinioncount_yay').get()
    most_nayed = models.Song.all().order('-opinioncount_nay').get()
    
    data = {
      'Most Viewed': most_viewed.json(),
      'Most Yayed': most_yayed.json(),
      'Most Nayed': most_nayed.json()}
    
    self.response.out.write(simplejson.dumps(data))
 
class GetRecentPlaylist(webapp.RequestHandler):
  def post(self):
    pass
