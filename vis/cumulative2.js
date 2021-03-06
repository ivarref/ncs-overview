var d3 = require("d3");
var findGetParameter = require('./findgetparameter.js');
require('./style.css');

function show_resource(config) {
    d3.formatDefaultLocale({
        'decimal': ',',
        'thousands': '.',
        'grouping': [3],
        'currency': ['$', '']
    });

    var svg = d3.select('body').append('svg')
        .attr('width', 960)
        .attr('height', 500)

    var margin = { top: 40, right: 50, bottom: 40, left: 50 },
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var parseTime = d3.timeParse("%Y");

    var x = d3.scaleTime()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var colorscheme = require('./colors_region.js').colors;
    var z = d3.scaleOrdinal(colorscheme);
    var stack = d3.stack();

    var area = d3.area()
        .x(function (d, i) { return x(d.data.date); })
        .y0(function (d) { return y(d[0]); })
        .y1(function (d) { return y(d[1]); });

    d3.csv(config.filename,
        function (d) {
            d.date = parseTime(d.year);
            d.reserveOil = +d.reserveOil;
            d.reserveGas = +d.reserveGas;
            d.reserveOE = +d.reserveOE;
            d.producedOil = +d.producedOil;
            d.producedGas = +d.producedGas;
            d.producedOE = +d.producedOE;
            d.Sum = 0;
            config.keys.forEach(function (k) {
                d.Sum += d[k];
            })
            return d;
        },
        function (error, data) {
            if (error) throw error;
            var keys = config.keys;

            x.domain(d3.extent(data, function (d) { return d.date; }));
            y.domain([0, d3.max(data, function (d) { return d.Sum; })]);
            z.domain(keys);
            stack.keys(keys);
            var endData = data[data.length - 1];

            var layer = g.selectAll(".layer")
                .data(stack(data))
                .enter().append("g")
                .attr("class", "layer");

            layer.append("path")
                .attr("class", "area")
                .style("fill", function (d) { return z(d.key); })
                .attr("d", area);

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
                .classed('biggertext', true)
                .text(config.unit);

            g.append("g")
                .attr("transform", "translate(" + width + ",0)")
                .call(d3.axisRight(y))
                .append("g")
                .attr("transform", "translate(0," + (height / 2) + ")")
                .append("text")
                .attr("fill", "#000")
                .attr("transform", "rotate(90)")
                .attr("y", -margin.right + 8)
                .attr("dy", "0.71em")
                .style("text-anchor", "middle")
                .classed('biggertext', true)
                .text(config.unit);

            g.append("g")
                .append("text")
                .attr('dy', '-.35em')
                .attr('x', width / 2)
                .style("text-anchor", "middle")
                .classed("heading", true)
                .text("Norsk " + config.title + ": Kumulativ produksjon og reservevekst sidan år " + data[0].date.getFullYear())

            var legend = g.append("g")
                .attr("transform", "translate(15,15)")
                .selectAll('g')
                .data(keys.slice(0).reverse())
                .enter().append('g')
                .attr("transform", function (d, i) { return "translate(0," + (i * 20) + ")"; })

            legend
                .append('rect')
                .attr('width', 18)
                .attr('height', 18)
                .attr('fill', z);

            var translate = {
                'Norwegian sea': 'Norskehavet',
                'North sea': 'Nordsjøen',
                'Barents sea': 'Barentshavet'
            };

            legend.append('text')
                .attr("x", 18 + 4)
                .attr('y', 9)
                .attr("dy", "0.35em")
                .classed('biggertext', true)
                .text(function (d) {
                    if (d.indexOf("reserve") != -1) {
                        return "Kumulativ reservevekst (brutto, nye felt sidan " + data[0].date.getFullYear() + ")";
                    } else {
                        return "Kumulativ produksjon (sidan " + data[0].date.getFullYear() + ")";
                    }
                });

            var format = function (x) {
                return x.toFixed(1).replace(".", ",");
            };

            var lines =
                [
                    "Sidan år {år} har nye felt gjeve ein reservevekst på {reservar} {unit}."
                        .replace("{unit}", config.unit.toLowerCase())
                        .replace("{år}", data[0].date.getFullYear())
                        .replace("{reservar}", format(endData[config.keys[1]])),
                    "I den samme perioden har ein produsert {produsert} {unit}."
                        .replace("{unit}", config.unit.toLowerCase())
                        .replace("{år}", data[0].date.getFullYear())
                        .replace("{produsert}", format(endData[config.keys[0]]))
                    ,

                    "Ein har dermed produsert {x} gonger så mykje som ein har funne."
                        .replace("{x}", format(endData[config.keys[0]] / endData[config.keys[1]]))
                ];
            g.append("g")
                .attr("transform", "translate(15,75)")
                .selectAll('g')
                .data(lines)
                .enter().append('g')
                .attr("transform", function (d, i) { return "translate(0," + (i * 20) + ")"; })
                .append('text')
                .classed('biggertext', true)
                .text(Object)

      g.append("g")
          .attr("transform", "translate(" + 0 + "," + (height+margin.bottom) + ")")
          .append('text')
          .classed('biggertext', true)
          .attr('dy', '-.31em')
          .style('text-anchor', 'start')
          .text("Basert på data frå Oljedirektoratet")

        g.append("g")
          .attr("transform", "translate(" + width + "," + (height+margin.bottom) + ")")
          .append('text')
          .classed('biggertext', true)
          .attr('dy', '-.31em')
          .style('text-anchor', 'end')
          //.style('font-variant', 'small-caps')
          .text("Diagram: Refsdal.Ivar@gmail.com")

        });
}

var m = {
    oil: {
        title: 'olje',
        unit: 'Milliardar fat olje',
        keys: ['producedOil', 'reserveOil'],
        screenshot: 'cumulative_oil_production_vs_reserve_growth_since_2000.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_2000_gboe.csv'
    },
    oil1990: {
        title: 'olje',
        unit: 'Milliardar fat olje',
        keys: ['producedOil', 'reserveOil'],
        screenshot: 'cumulative_oil_production_vs_reserve_growth_since_1990.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_1990_gboe.csv'
    },
    gas: {
        title: 'gass',
        unit: 'Milliardar fat oljeekvivalentar',
        keys: ['producedGas', 'reserveGas'],
        screenshot: 'cumulative_gas_production_vs_reserve_growth_since_2000.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_2000_gboe.csv'
    },
    gas1990: {
        title: 'gass',
        unit: 'Milliardar fat oljeekvivalentar',
        keys: ['producedGas', 'reserveGas'],
        screenshot: 'cumulative_gas_production_vs_reserve_growth_since_1990.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_1990_gboe.csv'
    },
    oe: {
        title: 'petroleum',
        unit: 'Milliardar fat oljeekvivalentar',
        keys: ['producedOE', 'reserveOE'],
        screenshot: 'cumulative_oe_production_vs_reserve_growth_since_2000.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_2000_gboe.csv'
    },
    oe1990: {
        title: 'petroleum',
        unit: 'Milliardar fat oljeekvivalentar',
        keys: ['producedOE', 'reserveOE'],
        screenshot: 'cumulative_oe_production_vs_reserve_growth_since_1990.png',
        filename: '/data/cumulative/cumulative_reserves_vs_production_since_1990_gboe.csv'
    },
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode]);