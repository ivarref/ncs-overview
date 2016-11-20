var d3 = require("d3");
require('./style.css');

function isNumeric(num) {
    return !isNaN(num);
}

function isGroup(v) {
    return v!=='Date' && v!=='date' && v!=='Sum';
}

function findGetParameter(parameterName, default_value) {
    var result = default_value,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function show_resource(resource, group, unit, file) {
    d3.formatDefaultLocale({
        'decimal': ',',
        'thousands': '.',
        'grouping': [3],
        'currency': ['$', '']
    })

    var svg = d3.select('body').append('svg')
        .attr('width', 960 / 1.5)
        .attr('height', 500 / 1.5)
        .style('border', "1px solid #000000");

    var margin = { top: 40, right: 20, bottom: 30, left: 50 },
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var parseTime = d3.timeParse("%Y");

    var x = d3.scaleTime()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var z = d3.scaleOrdinal(d3.schemeCategory10);

    var stack = d3.stack();

    var area = d3.area()
        .x(function (d, i) { return x(d.data.date); })
        .y0(function (d) { return y(d[0]); })
        .y1(function (d) { return y(d[1]); });

    d3.csv(file,
        function (d) {
            d.date = parseTime(d.Date);
            Object.keys(d).filter(isGroup).forEach(function (k) {
                d[k] = +d[k];
            });
            d.Sum = +d.Sum;
            return d;
        },
        function (error, data) {
            if (error) throw error;
            var keys = data.columns.filter(isGroup);

            x.domain(d3.extent(data, function (d) { return d.date; }));
            y.domain([0, d3.max(data, function (d) { return d.Sum; })]);
            z.domain(keys);
            stack.keys(keys);

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
                .text(unit);

            g.append("g")
                .append("text")
                .attr('dy', '-.35em')
                .attr('x', width / 2)
                .style("text-anchor", "middle")
                .classed("heading", true)
                .text("Norsk " + resource + " etter " + group)

            g.append('text')
                .attr("transform", "translate(15,7)")
                .attr("dy", "0.35em")
                .style('font-weight', 'bold')
                .text(group[0].toUpperCase() + group.substr(1))

            var legend = g.append("g")
                .attr("transform", "translate(15,15)")
                .selectAll('g')
                .data(keys.slice(0).reverse())
                .enter().append('g')
                .attr("transform", function (d, i) { return "translate(0," + (i * 20) + ")"; })
                .style("font", "10px sans-serif");

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
                .text(function (d) { return d in translate ? translate[d] : d });
        });
}

var m = {
    oil: {
        title: 'oljeproduksjon',
        unit: 'Millioner fat/dag',
        group: 'funntiår',
        filename: '/data/decade/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv'
    },
    gas: {
        title: 'gassproduksjon',
        unit: 'Millioner fat oljeekvivalenter/dag',
        group: 'funntiår',
        filename: '/data/decade/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv'
    },
    petroleum: {
        title: 'petroleumproduksjon',
        unit: 'Millioner fat oljeekvivalenter/dag',
        group: 'funntiår',
        filename: '/data/decade/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv'
    },
    oil_region: {
        title: 'oljeproduksjon',
        unit: 'Millioner fat/dag',
        group: 'region',
        filename: '/data/region/oil_production_yearly_12MMA_mboe_d_by_region.csv'
    },
    gas_region: {
        title: 'gassproduksjon',
        unit: 'Millioner fat oljeekvivalenter/dag',
        group: 'region',
        filename: '/data/region/gas_production_yearly_12MMA_mboe_d_by_region.csv'
    },
    petroleum_region: {
        title: 'petroleumproduksjon',
        unit: 'Millioner fat oljeekvivalenter/dag',
        group: 'region',
        filename: '/data/region/oe_production_yearly_12MMA_mboe_d_by_region.csv'
    }
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);

// show_resource('oljeproduksjon', 'Millioner fat/dag', '/data/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
// show_resource('gassproduksjon', 'Millioner fat oljeekvivalenter/dag', '/data/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
// show_resource('petroleumproduksjon', 'Millioner fat oljeekvivalenter/dag', '/data/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
