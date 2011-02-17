"""The main module that sets up URL handlers and runs the app.

This module uses the App Engine webapp library to assign
URL patterns to various classes. 
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import viewer_actions
import global_actions
import parser_actions
import pages

def main():
  application = webapp.WSGIApplication([
      ('/', pages.Player),
      ('/stats', pages.Stats),
      ('/action/parser/parse_playlist', parser_actions.ParsePlaylist),
      ('/action/viewer/get_song_stats', viewer_actions.GetSongStats),
      ('/action/viewer/update_song_stats', viewer_actions.UpdateSongStats),
      ('/action/global/get_song_stats', global_actions.GetSongStats),
	    ('/action/global/get_top_songs', global_actions.GetTopSongs),
	    ('/action/global/get_recent_playlist', global_actions.GetRecentPlaylist),
      ], debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()