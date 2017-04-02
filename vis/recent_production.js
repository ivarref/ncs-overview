var d3 = require("d3");
require('./style.css');

var findGetParameter = require('./findgetparameter.js');

function add_mma_line(svg, data, x, y) {
  var line = d3.line()
    .x(function (d) { return x(d.date) + (x.bandwidth() / 2.0); })
    .y(function (d) { return y(d.mma); });

  svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr("stroke-width", 3.5)
    .attr("d", line);

  var yearOnly = data.filter(function (x) { return x.date.getMonth() == 11; })
  var points = svg.append("g")
    .selectAll('g')
    .data(yearOnly)
    .enter()
    .append('g')
    .attr('transform', function (d) {
      return 'translate(' + (x(d.date) + (x.bandwidth() / 2.0)) + ',' + y(d.mma) + ')'
    })

  points.append('text')
    .attr('dy', '-1.71em')
    .style('text-anchor', 'middle')
    .text(function (d) { return (d.mma + "").replace(".", ",") })

  points.append('text')
    .attr('dy', '-.71em')
    .style('text-anchor', 'middle')
    .text(function (d) { return "(" + d.date.getFullYear() + ")" })

  points
    .append('circle')
    .attr('cx', 0)
    .attr('cy', 0)
    .style('stroke', 'black')
    .style('stroke-width', '2')
    .style('fill', 'yellow')
    .attr('r', '5')
}

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

  var margin = { top: 50, right: 50, bottom: 40, left: 50 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var parseTime = d3.timeParse("%Y-%m");

  d3.csv(file,
    function (d) {
      var o = Object.keys(d).reduce(function (o, n) { o[n] = +d[n]; return o; }, {});
      o.date = parseTime(d.date);
      o.datestr = d.date;
      return o;
    },
    function (error, data) {
      if (error) throw error;
      var remove = ['date', 'mma', 'datestr'];
      var keys = data.columns.filter(function (d) { return remove.indexOf(d) == -1 });
      keys = keys.sort()
      keys = keys.reverse()
      data = data.filter(function (x) { return x.datestr >= '2010-12'; })

      var cols = d3.schemeCategory10;
      console.log(cols);
      var cols = ["#d62728",  //red
        "#ff7f0e", //orange
        "#8c564b", //brown
        "#1f77b4", //blue
        "#17becf", //cyan
        "#e377c2", //pink
        "#9467bd", //purple
        "#bcbd22", //gusjegul
        "#7f7f7f", //gray
        "#2ca02c", //green
      ]
      var z = d3.scaleOrdinal()
        .range(cols);
      z.domain(keys);

      var y = d3.scaleLinear()
        .domain([0, d3.max(data.map(function (d) { return d3.max([d.mma]) }))])
        .range([height, 0]);

      svg.append("g")
        .append("text")
        .attr('dy', '-0.75em')
        .attr('x', width / 2)
        .style("text-anchor", "middle")
        .classed("heading", true)
        .text("Norsk oljeproduksjon etter feltmodenhet, 2010 - " + data[data.length - 1].date.getFullYear())

      var x = d3.scaleBand()
        .domain(data.map(function (d) { return d.date }))
        .paddingInner(0.05)
        //.align(0.1)
        .rangeRound([0, width]);

      var x2 = d3.scaleTime()
        .range([0, width]);

      svg.append("g")
        .selectAll("g")
        .data(d3.stack().keys(keys)(data))
        .enter().append("g")
        .attr("fill", function (d) { return z(d.key); })
        .selectAll("rect")
        .data(function (d) { return d; })
        .enter().append("rect")
        .attr("x", function (d) { return x(d.data.date); })
        .attr("y", function (d) { return y(d[1]); })
        .attr("height", function (d) { return y(d[0]) - y(d[1]); })
        .attr("width", x.bandwidth());

      var legendbox = svg.append("g")
        .attr('transform', 'translate(10, ' + (height - (20 * (1 + keys.length))) + ')')
      legendbox.append('rect')
        .attr('x', 20)
        .attr('y', -20)
        .attr('width', 170)
        .attr('height', 10 + 20 * (1 + keys.length))
        .attr('fill', 'white')
        .attr('stroke', 'black')
        .style('fill-opacity', '0.8')

      legendbox.append('text')
        .attr('x', 20 + 10)
        .style('font-weight', 'bold')
        .text('Prosent produsert')

      var legend = svg.append("g")
        .attr('transform', 'translate(20, ' + (5 + height - (20 * (1 + keys.length))) + ')')
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        //.attr("text-anchor", "end")
        .selectAll("g")
        .data(keys.slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

      legend.append("rect")
        .attr("x", 19)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", z);

      legend.append("text")
        .attr("x", 24 + 20)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function (d) { return d.slice(2); });

      var yearOnly = data.filter(function (x) { return x.date.getMonth() == 0; })

      x2.domain(d3.extent(data, function (d) { return d.date; }));
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x)
          .tickValues(yearOnly.map(function (d) { return d.date }))
          .tickFormat(function (d) { return "Jan " + d.getFullYear() }))

      svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 8)
        .attr("x", -height / 2)
        .attr("dy", "0.71em")
        .style("text-anchor", "middle")
        .text("Millionar fat olje/dag");

      svg.append("g")
        .attr("transform", "translate(" + width + ",0)")
        .call(d3.axisRight(y))
      // svg.append("g")
      // .append("text")
      // .attr("fill", "#000")
      // .attr("transform", "rotate(90)")
      // .attr("y", -margin.right + 4)
      // .attr("dy", "0.71em")
      // .style("text-anchor", "middle")
      // .text("Millionar fat olje/dag");


      add_mma_line(svg, data, x, y);
      svg.append("g")
        .attr("transform", "translate(" + 0 + "," + (height + margin.bottom) + ")")
        .append('text')
        .attr('dy', '-.31em')
        .style('text-anchor', 'start')
        .text("Basert på data frå Oljedirektoratet")

      svg.append("g")
        .attr("transform", "translate(" + width + "," + (height + margin.bottom) + ")")
        .append('text')
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
    filename: '/data/oil-production-bucket-stacked.csv',
    screenshot: 'oil_produced_reserves_by_discovery_decade.png'
  }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].unit_key, m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);
