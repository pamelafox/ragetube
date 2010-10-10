var LIKER = function() {
  // Constants for data attributes used throughout
  var DATA_LIKERID = 'data-likegroup';
  var DATA_LIKERTYPE = 'data-liketype';
  var DATA_LIKEVALUE = 'data-likevalue';

  // Create option for liker value
  function createLikerValue(id, value) {
    // Create span and add data attributes
    var span = document.createElement('span');
    span.setAttribute(DATA_LIKERID, id);
    span.setAttribute(DATA_LIKEVALUE, value);
    span.innerHTML = value;
    span.onclick = function() {
      handleValueClick(span);
    };
    // Set default styles and selected style if needed
    span.style.cursor = 'pointer';
    span.className = 'unselected';
    if (localStorage[id] == value) {
      span.className = value + ' selected';
    }
    return span;
  }

  // Function called when liker option is clicked
  function handleValueClick(elem) {
    // Retrieve the ID of liker and value, save
    var likerId = elem.getAttribute(DATA_LIKERID);
    var likeValue = elem.getAttribute(DATA_LIKEVALUE);
    localStorage[likerId] = likeValue;

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

  function supportsLocalStorage() {
    try {
      return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
      return false;
    }
  }

  return {
    // Create an interactive liker
    createLiker: function(id) {
      var div = document.createElement('div');
      if (!supportsLocalStorage()) return div;
      div.setAttribute(DATA_LIKERID, id);
      div.setAttribute(DATA_LIKERTYPE, 'full');
      var values = ['Yay', 'Meh', 'Nay'];
      for (var i = 0; i < values.length; i++) {
        div.appendChild(createLikerValue(id, values[i]));
        div.appendChild(document.createTextNode(' '));
      }
      return div;
    },
    // Create a read-only element that reflects like state
    createLikerMini: function(id) {
      var span = document.createElement('span');
      if (!supportsLocalStorage()) return span;
      span.setAttribute(DATA_LIKERID, id);
      span.setAttribute(DATA_LIKERTYPE, 'mini');
      var value = localStorage[id];
      if (value) {
        span.innerHTML = value;
        span.className = value;
      } else {
        span.innerHTML = '';
      }
      return span;
    }
  }
}();
