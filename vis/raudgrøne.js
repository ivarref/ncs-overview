var d3 = require("d3");
require('./style.css');

var findGetParameter = require('./findgetparameter.js');

function show_resource(file, who, from, to) {
  d3.formatDefaultLocale({
    'decimal': ',',
    'thousands': '.',
    'grouping': [3],
    'currency': ['$', '']
  })
  var svg = d3.select('body').append('svg')
    .attr('width', 960)
    .attr('height', 500);

  var margin = { top: 40, right: 20, bottom: 30, left: 50 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var parseTime = d3.timeParse("%Y-%m");
  var x = d3.scaleTime()
    .range([0, width]);
  var y = d3.scaleLinear()
    .range([height, 0]);

  d3.csv(file,
    function (d) {
      return {
        'dateStr': d.Date,
        'date': parseTime(d.Date),
        
        'Sum': +d['Sum']
      };
    },
    function (error, data) {
      if (error) throw error;
      data = data.filter(function (d) { return d.dateStr >= from && d.dateStr <= to })

      x.domain(d3.extent(data, function (d) { return d.date; }));
      y.domain([0, d3.max(data, function (d) { return d.Sum; })]);

      var start = data[0].Sum;
      var stop = data[data.length - 1].Sum;
      var auke = (((stop / start) * 100.0) - 100.0).toFixed(0);

      g.append("g")
        .append("text")
        .attr('dy', '-.35em')
        .attr('x', width / 2)
        .style("text-anchor", "middle")
        .classed("heading", true)
        .text("Norsk gassproduksjon opp " + auke + "% " + who)

      var monthNames = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"];
      //                     0         1         2      3       4       5       6       7          8           9          10          11
      //                     1         2         3      4       5       6       7       8          9          10          11          12
      function formatDate(d) {
        return monthNames[d.getMonth()] + " " + d.getFullYear();
      }

      var startData = data[0];
      var endData = data[data.length - 1];
      console.log(startData)

      g.append("g")
        .append("text")
        .attr('dy', '-.35em')
        .attr('y', 15)
        .attr('x', width / 2)
        .style("text-anchor", "middle")
        .text(function (d) { return formatDate(startData.date) + " - " + formatDate(endData.date) })

      var area = d3.area()
        .x(function (d) { return x(d.date) })
        .y0(function (d) { return y(0) })
        .y1(function (d) { return y(d.Sum) })

      g.append('g')
        .append('path')
        .datum(data)
        .attr('d', area)
        .style('fill', 'steelblue')

      var v = data[0];

      g.append("g")
        .attr('transform', 'translate(0,' + y(v.Sum) + ')')
        .append("text")
        .attr('dy', '.25em')
        .attr('dx', '.25em')
        .attr('y', 15)
        .style('fill', 'white')
        .text(formatDate(startData.date) + " = " + v.Sum.toFixed(2).replace('.', ',') + " Mill. fat o.e./dag")

      v = data[data.length - 1];

      g.append("g")
        .attr('transform', 'translate(' + x(v.date) + ',' + y(v.Sum) + ') rotate(-25)')
        .append("text")
        .attr('dy', '.45em')
        .attr('dx', '-1.25em')
        .style('fill', 'white')
        .style("text-anchor", "end")
        .text(formatDate(endData.date) + " = " + v.Sum.toFixed(2).replace('.', ',') + " Mill. fat o.e./dag")

      g.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      g.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 8)
        .attr("x", -height / 2)
        .attr("dy", "0.71em")
        .style("text-anchor", "middle")
        .text("Millionar fat oljeekvivalentar/dag");
    });
}

var m = {
  raudgrone: {
    file: '/data/decade/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv',
    who: 'under den raud-grøne regjeringa',
    from: '2005-10',
    to: '2013-10',
    screenshot: 'gassproduksjon_raudgrøne.png',
  },
  sidantotusen: {
    file: '/data/decade/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv',
    who: 'sidan år 2000',
    from: '2000-01',
    to: '3000-01',
    screenshot: 'gassproduksjon_sidan_2000.png'
  },
  erna: {
    file: '/data/decade/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv',
    who: 'under Høgre-FrP',
    from: '2013-09',
    to: '3000-01',
    screenshot: 'gassproduksjon_høgre_frp.png'
  },
};

var mm = m[findGetParameter('mode', 'raudgrone')];
show_resource(mm.file, mm.who, mm.from, mm.to);
