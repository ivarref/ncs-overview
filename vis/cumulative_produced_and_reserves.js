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
    svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(file,
    function (d) {
      return { 
        'name' : d['name'],
        'origRecoverable': +d['origRecoverable' + unit_key], 
        'produced': +d['origRecoverable' + unit_key] - +d['remaining' + unit_key],
        'remaining': +d['remaining' + unit_key],
      };
    },
    function (error, data) {
      if (error) throw error;
      data = data.filter(function(d) { return d.name !== 'Sum'; });
      var keys = data.map(function(d) { return d.name });
      console.log("keys is", keys);

      var y = d3.scaleLinear()
        .domain([0, d3.max(data.map(function(d) { return d.origRecoverable }))])
        .range([height, 0]);

      var colorscheme = group === 'funntiår' ? d3.schemeCategory10 : ["#bcbd22", "#17becf", "#e377c2"];

      var bar = svg.selectAll('g')
        .data(data)
        .enter()
        .append('g')
        .attr('transform', function(d, i) { return 'translate(' + i*50 + ',0)'; });
      
      bar.append('g')
      .append('rect')
      .attr('width', 15)
      .attr('y', function(d) { return y(d.remaining)} )
      .attr('height', function(d) { return height - y(d.remaining)} )
      .style('fill', function(d, i) { return colorscheme[i] })

      bar.append('g')
      .append('rect')
      .attr('width', 15)
      .attr('y', function(d) { return y(d.origRecoverable)} )
      .attr('height', function(d) { return height - y(d.produced) } )
      .style('fill', function(d, i) { return colorscheme[i] })
      .style('fill-opacity', '0.5')

      bar
        .append('text')
        .style('text-anchor', 'middle')
        .attr('dx', 15/2)
        .text(function(d) { return d.name })

      svg.append("g")
                .call(d3.axisLeft(y))
                .append("text")
                .attr("fill", "#000")
                .attr("transform", "rotate(-90)")
                .attr("y", -margin.left + 8)
                .attr("x", -height / 2)
                .attr("dy", "0.71em")
                .style("text-anchor", "middle")
                .text(unit);

    });
}

var m = {
  oil: {
    title: 'Olje',
    unit: 'Milliarder fat',
    unit_key: 'Oil',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  },
  gas: {
    title: 'Gass',
    unit: 'Milliarder fat oljeekvivalenter',
    unit_key: 'Gas',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].unit_key, m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);

// var data = require('../data/decade/reserves_gboe_by_decade.json');
// console.log('start data...');
// console.log(data);
// console.log('end data...');
