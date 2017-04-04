var d3 = require("d3");
require('./style.css');

var findGetParameter = require('./findgetparameter.js');

function show_resource(opts) {
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

  var margin = { top: 70, right: 60, bottom: 60, left: 60 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    svg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(opts.filename,
    function (d) {
      return Object.keys(d).reduce(function (o, n) {
        var v = d[n] == "" ? NaN : (+d[n] / 1000.0);
        o[n] = v;
        return o;
      }, {});
    },
    function (error, data) {
      if (error) throw error;
      var xstart = 120;
      var keys = data.columns;

      svg.append("g")
        .append("text")
        .attr('dy', '-1.75em')
        .attr('x', xstart)
        .style("text-anchor", "start")
        .classed("heading", true)
        .text(opts.title)

      svg.append("g")
        .append("text")
        .attr('dy', '-1.35em')
        .attr('x', xstart)
        .style("text-anchor", "start")
        .text('Funn = reservar + (alle) betinga ressursar')

      var x = d3.scaleLinear()
        .domain([1, data.length])
        .range([0, width])

      var y = d3.scaleLinear()
        .domain([0, d3.max(Object.values(data[data.length - 1]))])
        .range([height, 0])

      var line = d3.line()
        .x(function (d, i) { return x(i); })
        .y(function (d) { return y(d); });

      var region = svg.append("g")
        .selectAll('g')
        .data(keys)
        .enter().append('g')

      var cols = [
        "#e377c2", //pink
        //        "#8c564b", //brown
        "#2ca02c", //green
        //        "#d62728", //red
        "#ff7f0e", //orange


        "#1f77b4", //blue
        "#17becf", //cyan
        "#bcbd22", //gusjegul
        "#9467bd", //purple
        "#7f7f7f", //gray
      ]

      var values = keys.reduce(function (o, d) {
        var vals = data.map(function (v) { return v[d]; });
        vals = vals.filter(function (v) { return !isNaN(v) });
        o[d] = vals
        return o;
      }, {});

      region.append('path')
        .attr('class', 'line')
        .attr('d', function (d) { return line(values[d]) })
        .attr("fill", "none")
        .attr("stroke", function (d, i) { return cols[i] })
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 3.5)

      function last(vals) {
        return vals[vals.length - 1];
      };

      function fmt(v) {
        var s = v.toFixed(2);
        return s.replace(".", ",");
      }

      function gj(v) {
        return fmt((1000.0 * v[v.length - 1]) / v.length);
      }

      var k = 'Norwegian sea';
      svg.append('g')
        .attr('transform', 'translate(' + x(values[k].length) + ',' + y(last(values[k])) + ')')
        .append('text')
        .attr('dx', '.31em')
        .attr('dy', '.31em')
        .text('Norskehavet, ' + fmt(last(values[k])) + " mrd. fat.");
      svg.append('g')
        .attr('transform', 'translate(' + x(values[k].length) + ',' + y(last(values[k])) + ')')
        .append('text')
        .attr('dx', '.31em')
        .attr('dy', '1.41em')
        .text("Funn per brønn: " + gj(values[k]) + " mill. fat.")



      k = 'Barents sea'
      svg.append('g')
        .attr('transform', 'translate(' + x(values[k].length) + ',' + y(last(values[k])) + ')')
        .append('text')
        .attr('dx', '.31em')
        .attr('dy', '.31em')
        .text('Barentshavet, ' + fmt(last(values[k])) + " mrd. fat. Funn per brønn: " + gj(values[k]) + " mill. fat.")

      var k = 'North sea';
      var val = values[k]
      var idx = Math.floor(val.length / 2);
      svg.append('g')
        .attr('transform', 'translate(' + x(val.length / 2) + ',' + y(val[idx]) + ')')
        .append('text')
        .attr('dx', '.31em')
        .attr('dy', '1.31em')
        .text('Nordsjøen, ' + fmt(last(values[k])) + " mrd. fat.")
      svg.append('g')
        .attr('transform', 'translate(' + x(val.length / 2) + ',' + y(val[idx]) + ')')
        .append('text')
        .attr('dx', '.31em')
        .attr('dy', '2.41em')
        .text("Funn per brønn: " + gj(values[k]) + " mill. fat.")

      var xstart = 10;
      var ystart = 10;
      var legendbox = svg.append("g")
        .attr('transform', 'translate(' + xstart + ',' + ystart + ')')
      legendbox.append('rect')
        .attr('width', 148)
        .attr('height', 20 * (1 + keys.length) + 10.0)
        .attr('fill', 'white')
        .attr('stroke', 'black')
        .style('fill-opacity', '0.8')

      legendbox = legendbox.append('g')
        .attr('transform', 'translate(' + 7 + ',' + 20 + ')')

      legendbox.append('text')
        .style('font-weight', 'bold')
        .text('Region')

      var legend = legendbox.append("g")
        .attr('transform', 'translate(0, 5)')
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .selectAll("g")
        .data(keys)
        .enter().append("g")
        .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

      legend.append("rect")
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", function (d, i) { return cols[i] });

      var translate = {
        'Norwegian sea': 'Norskehavet',
        'North sea': 'Nordsjøen',
        'Barents sea': 'Barentshavet'
      };

      legend.append("text")
        .attr("x", 25)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function (d) { return translate[d]; });

      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))

      svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 3)
        .attr("x", -height / 2)
        .attr("dy", "0.71em")
        .style("text-anchor", "middle")
        .text("Milliardar fat oljeekvivalentar");

      svg.append("g")
        .attr("transform", "translate(" + width + ",0)")
        .call(d3.axisRight(y))
        .append("g")
        .attr("transform", "translate(0," + (height / 2) + ")")
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(90)")
        .attr("y", -margin.right + 4)
        .attr("dy", "0.71em")
        .style("text-anchor", "middle")
        .text("Milliardar fat oljeekvivalentar");

      svg.append("g")
        .attr("transform", "translate(" + (width / 2.0) + "," + (height) + ")")
        .append('text')
        .attr('dy', '2.41em')
        .style('text-anchor', 'middle')
        .text("Antall leitebrønnar")

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
    filename: '/data/wellbores_cumulative_recoverable_plus_resources_oil_mboe.csv',
    title: 'Norsk olje: Kumulative funn etter region',
    screenshot: 'cumulative_discoveries_oil_wellbores_by_region.png'
  },
  gas: {
    filename: '/data/wellbores_cumulative_recoverable_plus_resources_gas_mboe.csv',
    title: 'Norsk gass: Kumulative funn etter region',
    screenshot: 'cumulative_discoveries_gas_wellbores_by_region.png'
  },
  oe: {
    filename: '/data/wellbores_cumulative_recoverable_plus_resources_oe_mboe.csv',
    title: 'Norsk petroleum: Kumulative funn etter region',
    screenshot: 'cumulative_discoveries_oe_wellbores_by_region.png'
  }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode]);
