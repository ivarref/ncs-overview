var d3 = require("d3");
require('./style.css');

var findGetParameter = require('./findgetparameter.js');

function show_resource(unit_key, resource, group, unit, file) {
  d3.formatDefaultLocale({
    'decimal': ',',
    'thousands': '.',
    'grouping': [3],
    'currency': ['$', '']
  });

  var svg = d3.select('body').append('svg')
    .attr('width', 960 / 1.5)
    .attr('height', 500 / 1.5)
    .style('border', "1px solid #000000");

  var margin = { top: 40, right: 20, bottom: 30, left: 50 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(file,
    function (d) {
      return { 
        'name' : d['name'], 
        'produced': +d['origRecoverable' + unit_key] - +d['remaining' + unit_key],
        'remaining': +d['remaining' + unit_key],
      };
    },
    function (error, data) {
      if (error) throw error;
      data = data.filter(function(d) { return d.name !== 'Sum'; });
      var keys = data.map(function(d) { return d.name });
      console.log(data[0]);
      console.log(keys);
    });
}

var m = {
  oil: {
    title: 'Olje',
    unit: 'Milliarder fat',
    unit_key: 'Oil',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].unit_key, m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);
