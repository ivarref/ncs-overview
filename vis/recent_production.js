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
    .attr('width', 960)
    .attr('height', 500)
    .style('border', "1px solid #000000")

  var margin = { top: 40, right: 50, bottom: 40, left: 50 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var parseTime = d3.timeParse("%Y-%m");

  d3.csv(file,
    function (d) {
      return {
        'date': parseTime(d.date),
        'mboed': +d.mboed,
        'mma': +d.mma
      };
    },
    function (error, data) {
      if (error) throw error;
      data = data.filter(function (x) { return x.date.getFullYear() >= 2005; })
      var y = d3.scaleLinear()
        .domain([0, d3.max(data.map(function (d) { return d3.max([d.mboed, d.mma]) }))])
        .range([height, 0]);

      var x = d3.scaleBand()
        .domain(data.map(function (d) { return d.date }))
        .padding(0)
        .rangeRound([0, width]);


      var x2 = d3.scaleTime()
        .range([0, width]);

      x2.domain(d3.extent(data, function (d) { return d.date; }));
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x2));

      svg.append("g")
        .call(d3.axisLeft(y))

      svg.append("g")
        .attr("transform", "translate(" + width + ",0)")
        .call(d3.axisRight(y))

      var barWidth = width / data.length;
      console.log(barWidth);

      var bar = svg.append('g').selectAll('g')
        .data(data)
        .enter()
        .append('g')
        .attr('transform', function (d) { return 'translate(' + x(d.date) + ',0)'; });

      bar.append('g')
        .append('rect')
        .attr('width', x.bandwidth())
        .attr('y', function (d) { return y(d.mboed) })
        .attr('height', function (d) { return height - y(d.mboed) })
        .style('fill', 'steelblue')

      var line = d3.line()
        .x(function (d) { return x(d.date) + (x.bandwidth() / 2.0); })
        .y(function (d) { return y(d.mma); });

      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "orange")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 3.5)
        .attr("d", line);

      // var yearOnly = data.filter(function(x) { return x.date.getMonth() == 11; })
      // svg.append("g")
      // .selectAll('circle')
      // .data(yearOnly)
      // .enter()
      // .append('circle')
      // .attr('cx', function(d) { return x(d.date) + (x.bandwidth()/2.0) })
      // .attr('cy', function(d) { return y(d.mma) })
      // .attr('r', '5')

      svg.append("g")
        .attr("transform", "translate(" + 0 + "," + (height + margin.bottom) + ")")
        .append('text')
        .classed('biggertext', true)
        .attr('dy', '-.31em')
        .style('text-anchor', 'start')
        .text("Basert på data frå Oljedirektoratet")

      svg.append("g")
        .attr("transform", "translate(" + width + "," + (height + margin.bottom) + ")")
        .append('text')
        .classed('biggertext', true)
        .attr('dy', '-.31em')
        .style('text-anchor', 'end')
        .text("Diagram: Refsdal.Ivar@gmail.com")
    });
}

var m = {
  oil: {
    title: 'Olje',
    unit: 'Milliardar fat olje',
    unit_key: 'Oil',
    group: 'funntiår',
    filename: '/data/recent-oil-production-monthly.csv',
    screenshot: 'oil_produced_reserves_by_discovery_decade.png'
  }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].unit_key, m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);
