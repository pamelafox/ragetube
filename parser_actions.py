import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache

from django.utils import simplejson

import parser

class ParsePlaylist(webapp.RequestHandler):

  def post(self):
    url = self.request.get('url')
    playlist_info = memcache.get(url)
    if playlist_info is None:
      playlist_title, playlist_songs = parser.parse_url(url)
      playlist_info = {'title': playlist_title, 'songs': playlist_songs}
      memcache.set(url, simplejson.dumps(playlist_info), 60*60)
    else:
      playlist_info = simplejson.loads(playlist_info)
    self.response.out.write(simplejson.dumps(playlist_info))
