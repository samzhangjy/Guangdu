/*
 * @Author: Sam Zhang
 * @Date:   2020-04-12 14:20:57
 * @Last Modified by:   Sam Zhang
 * @Last Modified time: 2020-04-12 17:08:21
 */

function getTheme() {
  /* Get the theme cookies */
  var name = "theme=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length);
    }
  }
  return "light";
}

function changeTheme() {
  /* Set cookies for the current theme */
  var cvalue = getTheme();
  if (cvalue == "light") {
    document.cookie = "theme=dark;domain=" + document.domain;
  } else {
    document.cookie = "theme=light;domain=" + document.domain;
  }
}

function loadTheme() {
  /* Create a link element to load Bootstrap4 themes */
  var link = document.createElement("link");
  var theme = getTheme();
  linrk.rel = "stylesheet";
  link.href = "../../static/" + theme + ".min.css";
  document.getElementsByTagName("head")[0].appendChild(link);
  location.reload();
  document.getElementsByTagName("body")[0].removeChild(document.getElementById("scriptTheme"))
  location.reload();
}