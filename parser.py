import logging
import urllib2
import re
import string

from BeautifulSoup import BeautifulSoup

# Examples of theoretically parseable URLs
TEST_URLS = ['http://www.abc.net.au/rage/archive/s3130203.htm',
             'http://www.abc.net.au/rage/playlist/archive/2001/20010105.htm',
             'http://www.abc.net.au/triplej/hottest100/10/countdown/cd_list.htm',
             'http://www.abc.net.au/triplej/hottest100_alltime/countdown/cd_list.htm',
             'http://www.abc.net.au/triplej/hottest100_08/history/2007.htm',
             'http://www.abc.net.au/triplej/hottest100_08/history/2001.htm']
             
def parse_url(url):
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    if url == 'http://www.abc.net.au/triplej/hottest100/10/countdown/cd_list.htm':
      return parse_j2010(html)
    elif url == 'http://www.abc.net.au/triplej/hottest100_alltime/countdown/cd_list.htm':
      return parse_j2009(html)
    elif url.find('http://www.abc.net.au/triplej/hottest100_08/history/') > -1:
      year = int(url.split('/history/')[1].split('.htm')[0])
      if year > 2006:
        return parse_j2007(html)
      else:
        return parse_j2006(html)
    elif url.find('rage/playlist/') > -1:
      return parse_rage_old(html)
    else:
      return parse_rage(html)
  except urllib2.HTTPError, e:
    print e.code
    print e.read()

# pre 2007
def parse_j2006(html):
  soup = BeautifulSoup(html)
  playlist_title = soup.find('div', {'class': 'history-alpha'}).h2.string
  playlist = soup.find('div', {'class': 'list-100'})
  playlist_info = []
  for item in playlist:
    #print item
    #print type(item)
    if hasattr(item, 'class') and item.get('class') == 'numbers':
      # starting a new song
      artist = string.strip(item.nextSibling.string)
      title = item.nextSibling.nextSibling.split('-')
      if len(title) == 1:
        continue
      title = string.strip(title[1])
      song_info = {'artist': artist, 'title': title}
      playlist_info.append(song_info)
  return playlist_title, playlist_info
    
# 2007, 2008
def parse_j2007(html):
  soup = BeautifulSoup(html)
  playlist_title = soup.find('div', {'class': 'history-alpha'}).h2.string
  rows = soup.find('table').findAll('tr')
  playlist_info = []
  for row in rows:
    cells = row.findAll('td')
    artist = ''
    # Some cells have <br> in them
    for thing in cells[1].strong:
      if thing.string:
        artist += thing.string
    artist = string.strip(artist)
    title = string.strip(cells[2].string)
    if len(artist) == 0 or len(title) == 0:
      continue
    song_info = {'artist': artist, 'title': title}
    playlist_info.append(song_info)
  return playlist_title, playlist_info
  
  
def parse_j2009(html):
  soup = BeautifulSoup(html)
  playlist_title = 'Triple J Hottest 100: 2009'
  rows = soup.find('ul', {'class': 'printlist'}).findAll('li')
  playlist_info = []
  for row in rows:
    if row.string.find('-') == -1: #Number
      continue
    split_info = row.string.split(' - ')
    artist = split_info[0]
    title = split_info[1]
    song_info = {'title': string.strip(title), 'artist': string.strip(artist)}
    playlist_info.append(song_info)
  return playlist_title, playlist_info
  
  
def parse_j2010(html):
  soup = BeautifulSoup(html)
  playlist_title = 'Triple J Hottest 100: 2010'
  rows = soup.find('ul', {'id': 'cd_list'}).findAll('li')
  playlist_info = []
  for row in rows:
    split_info = row.string.split(' - ')
    if len(split_info) < 2: # Just in case
      continue
    artist = split_info[0]
    artist = re.sub('^[0-9]*\.', '', artist) # Replace countdown #s
    title = split_info[1]
    song_info = {'title': string.strip(title), 'artist': string.strip(artist)}
    playlist_info.append(song_info)
  return playlist_title, playlist_info
    
    
def parse_rage_old(html):
  soup = BeautifulSoup(html)
  table = soup.findAll('table')[1]
  rows = table.findAll('tr')
  playlist_title = rows[0].td.font.b.string
  rows = rows[2:]
  songs_info = []
  for row in rows:
    cells = row.findAll('td')
    if len(cells) < 2: # Skip blank rows
      continue
    info_cell = cells[1].find('font').contents[0]
    if type(info_cell) != type(playlist_title): # Skip links
      continue
    split_info = info_cell.split(' - ')
    if len(split_info) < 2: # Just in case
      continue
    title = string.strip(split_info[0])
    title = re.sub('^[0-9]*\.', '', title) # Replace countdown #s
    artist = string.strip(split_info[1])
    song_info = {'title': title, 'artist': artist}
    songs_info.append(song_info)
  return playlist_title, songs_info
  
  
def parse_rage(html):
  soup = BeautifulSoup(html)
  playlist_title = soup.find('p', {'class': 'date'}).string.replace('&nbsp;', '')
  playlist = soup.find("div", { "class" : "playlist" })
  sublists = playlist.findAll('p', {'class': 'list'})
  songs_info = []
  for sublist in sublists:
    if sublist.find('strong'):
      artists = sublist.findAll('strong')
      titles = sublist.findAll('em')
      for x in range(len(artists)):
        artist = artists[x].string
        if artist.find(' - LIVE') > -1:
          artist = artist.split(' - LIVE')[0]
        #TODO: split featuring?
        song_info = {'artist': string.strip(artist), 'title': string.strip(titles[x].string)}
        songs_info.append(song_info)
  return playlist_title, songs_info


             