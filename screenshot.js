var page = require('webpage').create();
page.open('http://localhost:8080/bundle', function() {
  page.render('screenshot.png');
  phantom.exit();
});