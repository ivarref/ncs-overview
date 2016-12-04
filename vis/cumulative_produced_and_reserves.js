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
  //.style('border', "1px solid #000000")


  var margin = { top: 40, right: 20, bottom: 30, left: 50 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(file,
    function (d) {
      var translate = {
        'Norwegian sea': 'Norskehavet',
        'North sea': 'Nordsjøen',
        'Barents sea': 'Barentshavet'
      };

      return {
        'name': d['name'] in translate ? translate[d['name']] : d['name'],
        'origRecoverable': +d['origRecoverable' + unit_key],
        'produced': +d['origRecoverable' + unit_key] - +d['remaining' + unit_key],
        'remaining': +d['remaining' + unit_key],
      };
    },
    function (error, data) {
      if (error) throw error;
      data = data.filter(function (d) { return d.name !== 'Sum'; });
      var keys = data.map(function (d) { return d.name });

      var y = d3.scaleLinear()
        .domain([0, d3.max(data.map(function (d) { return d.origRecoverable }))])
        .range([height, 0]);

      var x = d3.scaleBand()
        .domain(data.map(function (d) { return d.name }))
        .padding(0.1)
        .rangeRound([0, width])

      var colorscheme = group === 'funntiår' ? d3.schemeCategory10 : ["#bcbd22", "#17becf", "#e377c2"];

      var barWidth = width / data.length;

      var bar = svg.append('g').selectAll('g')
        .data(data)
        .enter()
        .append('g')
        .attr('transform', function (d) { return 'translate(' + x(d.name) + ',0)'; });

      svg.append("g")
        .append("text")
        .attr('dy', '-.35em')
        .attr('x', width / 2)
        .style("text-anchor", "middle")
        .classed("heading", true)
        .text("Norsk " + resource.toLowerCase() + ": Produsert og reservar etter " + group)

      bar.append('g')
        .append('rect')
        .attr('width', x.bandwidth())
        .attr('y', function (d) { return y(d.remaining) })
        .attr('height', function (d) { return height - y(d.remaining) })
        .style('fill', function (d, i) { return colorscheme[i] })

      bar.append('g')
        .append('rect')
        .attr('width', x.bandwidth())
        .attr('y', function (d) { return y(d.origRecoverable) })
        .attr('height', function (d) { return height - y(d.produced) })
        .style('fill', function (d, i) { return colorscheme[i] })
        .classed('produced_soft', true)

      var w = 20;
      var legend_produced = svg.append("g")
        .attr("transform", "translate(" + (width - keys.length * w) + ",15)");

      legend_produced.append('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.5em')
        .attr('dy', '1.15em')
        .classed('legend_caption', true)
        .text('Produsert')

      legend_produced.selectAll('g')
        .data(keys.slice(0).reverse())
        .enter().append('g')
        .attr("transform", function (d, i) { return "translate(" + (i * w) + ", 0)"; })
        .classed('produced_soft', true)
        .style("font", "10px sans-serif")
        .append('rect')
        .attr('width', 18)
        .attr('height', 18)
        .attr('fill', function (d, i) { return colorscheme[i]; });

      var legend_reserves = svg.append("g")
        .attr("transform", "translate(" + (width - keys.length * w) + ",35)");

      legend_reserves.append('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.5em')
        .attr('dy', '1.15em')
        .classed('legend_caption', true)
        .text('Reservar')

      legend_reserves.selectAll('g')
        .data(keys.slice(0).reverse())
        .enter().append('g')
        .attr("transform", function (d, i) { return "translate(" + (i * w) + ", 0)"; })
        .style("font", "10px sans-serif")
        .append('rect')
        .attr('width', 18)
        .attr('height', 18)
        .attr('fill', function (d, i) { return colorscheme[i]; });

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

      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
    });
}

var m = {
  oil: {
    title: 'Olje',
    unit: 'Milliardar fat',
    unit_key: 'Oil',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  },
  gas: {
    title: 'Gass',
    unit: 'Milliardar fat oljeekvivalentar',
    unit_key: 'Gas',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  },
  petroleum: {
    title: 'Petroleum',
    unit: 'Milliardar fat oljeekvivalentar',
    unit_key: 'OE',
    group: 'funntiår',
    filename: '/data/decade/reserves_gboe_by_decade.csv'
  },
  oil_region: {
    title: 'Olje',
    unit: 'Milliardar fat',
    unit_key: 'Oil',
    group: 'region',
    filename: '/data/region/reserves_gboe_by_region.csv'
  },
  gas_region: {
    title: 'Gass',
    unit: 'Milliardar fat oljeekvivalentar',
    unit_key: 'Gas',
    group: 'region',
    filename: '/data/region/reserves_gboe_by_region.csv'
  },
  petroleum_region: {
    title: 'Petroleum',
    unit: 'Milliardar fat oljeekvivalentar',
    unit_key: 'OE',
    group: 'region',
    filename: '/data/region/reserves_gboe_by_region.csv'
  }
};

var mode = findGetParameter('mode', 'oil_region');
show_resource(m[mode].unit_key, m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);
