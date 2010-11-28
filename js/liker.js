var Liker = function(song, isMini) {
  var DATA_LIKERID = 'data-likerid';
  var DATA_LIKERTYPE = 'data-likertype';
  var DATA_LIKEVALUE = 'data-likevalue';
  
  var song = song;
  
  if (isMini) {
    return createLikerMini();
  } else {
    return createLiker();
  }
  
  function createLikerMini() {
    var span = document.createElement('span');
    span.setAttribute(DATA_LIKERID, song.id);
    span.setAttribute(DATA_LIKERTYPE, 'mini');
    var value = song.opinion;
    if (value) {
      span.innerHTML = value;
      span.className = value;
    } else {
      span.innerHTML = '';
    }
    return span;
  }
  
  function createLiker() {
    var div = document.createElement('div');
    div.setAttribute(DATA_LIKERID, song.id);
    div.setAttribute(DATA_LIKERTYPE, 'full');
    var values = ['Yay', 'Meh', 'Nay'];
    for (var i = 0; i < values.length; i++) {
      div.appendChild(createLikerValue(values[i]));
      div.appendChild(document.createTextNode(' '));
    }
    return div;
   };
    

  
  // Create option for liker value
  function createLikerValue(value) {
    // Create span and add data attributes
    var span = document.createElement('span');
    span.setAttribute(DATA_LIKERID, song.id);
    span.setAttribute(DATA_LIKEVALUE, value);
    span.innerHTML = value;
    span.onclick = function() {
      handleValueClick(span);
    };
    // Set default styles and selected style if needed
    span.style.cursor = 'pointer';
    span.className = 'unselected';
    if (song.opinion == value) {
      span.className = value + ' selected';
    }
    return span;
  }

  // Function called when liker option is clicked
  function handleValueClick(elem) {
    // Retrieve the ID of liker and value, save
    var likeValue = elem.getAttribute(DATA_LIKEVALUE);
    var likerId = elem.getAttribute(DATA_LIKERID);
    var baseUrl = '/action/viewer/update_song_stats?';
    var url = baseUrl + 'key_name=' + likerId;
	  AJAX.post(url + '&opinion=' + likeValue, null, function(){});
    song.opinion = likeValue;
    
    // Change the style of the liker nodes
    var siblings = elem.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {
      siblings[i].className = 'unselected';
    }
    elem.className = likeValue + ' selected';

    // Change the value of any mini likers
    var allSpans = document.getElementsByTagName('span');
    for (var i = 0; i < allSpans.length; i++) {
      var span = allSpans[i];
      if (span.getAttribute(DATA_LIKERID) == likerId
          && span.getAttribute(DATA_LIKERTYPE) == 'mini') {
          span.innerHTML = likeValue;
          span.className = likeValue;
      }
    }
  }
};
