var page = require('webpage').create();
var system = require('system');
address = system.args[1];
output = system.args[2];

page.open(address, function() {
  page.render(output);
  phantom.exit();
});