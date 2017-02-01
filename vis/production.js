var d3 = require("d3");
var findGetParameter = require('./findgetparameter.js');
require('./style.css');

function isGroup(v) {
    return v !== 'Date' && v !== 'date' && v !== 'Sum';
}


function show_resource(resource, group, unit, file) {
    d3.formatDefaultLocale({
        'decimal': ',',
        'thousands': '.',
        'grouping': [3],
        'currency': ['$', '']
    })

    var svg = d3.select('body').append('svg')
        .attr('width', 960)
        .attr('height', 500);

    var margin = { top: 40, right: 50, bottom: 40, left: 50 },
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var parseTime = d3.timeParse("%Y");

    var x = d3.scaleTime()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var colorscheme = group === 'funntiår' ? d3.schemeCategory10 : require('./colors_region.js').colors;
    var z = d3.scaleOrdinal(colorscheme);
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
            // g.append("g")
            //     .attr("transform", "translate(0," + 0 + ")")
            //     .call(d3.axisTop(x));

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
                .text(unit);

            g.append("g")
                .attr("transform", "translate(" + width + ",0)")
                .call(d3.axisRight(y))
                .append("g")
                .attr("transform", "translate(0," + (height/2) + ")")
                .append("text")
                .attr("fill", "#000")
                .attr("transform", "rotate(90)")
                .attr("y", -margin.right + 8)
                .attr("dy", "0.71em")
                .style("text-anchor", "middle")
                .classed('biggertext', true)
                .text(unit);


            var title = "Norsk " + resource + " etter " + group;
            if (resource.indexOf(" ") >= 0) {
                title = resource;
            }
            g.append("g")
                .append("text")
                .attr('dy', '-.35em')
                .attr('x', width / 2)
                .style("text-anchor", "middle")
                .classed("heading", true)
                .text(title)

            g.append('text')
                .attr("transform", "translate(15,7)")
                .attr("dy", "0.35em")
                .style('font-weight', 'bold')
                .classed('biggertext', true)
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
                .classed('biggertext', true)
                .text(function (d) { return d in translate ? translate[d] : d });

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
        title: 'oljeproduksjon',
        unit: 'Millionar fat olje/dag',
        group: 'funntiår',
        filename: '/data/decade/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
        screenshot: 'oil_production_yearly_12MMA_by_discovery_decade.png'
    },
    oil_startproduction: {
        title: 'oljeproduksjon',
        unit: 'Millionar fat olje/dag',
        group: 'startår',
        filename: '/data/millennium/oil_production_yearly_12MMA_mboe_d_by_startproduction.csv',
        screenshot: 'oil_production_yearly_12MMA_by_startproduction.png'
    },
    gas_startproduction: {
        title: 'gassproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'startår',
        filename: '/data/millennium/gas_production_yearly_12MMA_mboe_d_by_startproduction.csv',
        screenshot: 'gas_production_yearly_12MMA_by_startproduction.png'
    },
    petroleum_startproduction: {
        title: 'petroleumproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'startår',
        filename: '/data/millennium/oe_production_yearly_12MMA_mboe_d_by_startproduction.csv',
        screenshot: 'oe_production_yearly_12MMA_by_startproduction.png'
    },
    gas: {
        title: 'gassproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'funntiår',
        filename: '/data/decade/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
        screenshot: 'gas_production_yearly_12MMA_by_discovery_decade.png'
    },
    petroleum: {
        title: 'petroleumproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'funntiår',
        filename: '/data/decade/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
        screenshot: 'oe_production_yearly_12MMA_by_discovery_decade.png'
    },
    oil_region: {
        title: 'oljeproduksjon',
        unit: 'Millionar fat olje/dag',
        group: 'region',
        filename: '/data/region/oil_production_yearly_12MMA_mboe_d_by_region.csv',
        screenshot: 'oil_production_yearly_12MMA_by_region.png'
    },
    gas_region: {
        title: 'gassproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'region',
        filename: '/data/region/gas_production_yearly_12MMA_mboe_d_by_region.csv',
        screenshot: 'gas_production_yearly_12MMA_by_region.png'
    },
    petroleum_region: {
        title: 'petroleumproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'region',
        filename: '/data/region/oe_production_yearly_12MMA_mboe_d_by_region.csv',
        screenshot: 'oe_production_yearly_12MMA_by_region.png'
    },
    oil_giants: {
        title: 'oljeproduksjon',
        unit: 'Millionar fat olje/dag',
        group: 'feltstorleik',
        filename: '/data/giants/oil_production_yearly_12MMA_mboe_d_by_fieldsize.csv',
        screenshot: 'oil_production_yearly_12MMA_by_fieldsize.png'
    },
    gas_giants: {
        title: 'gassproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'feltstorleik',
        filename: '/data/giants/gas_production_yearly_12MMA_mboe_d_by_fieldsize.csv',
        screenshot: 'gas_production_yearly_12MMA_by_fieldsize.png'
    },
    oe_giants: {
        title: 'petroleumproduksjon',
        unit: 'Millionar fat oljeekvivalentar/dag',
        group: 'feltstorleik',
        filename: '/data/giants/oe_production_yearly_12MMA_mboe_d_by_fieldsize.csv',
        screenshot: 'oe_production_yearly_12MMA_by_fieldsize.png'
    },
    oil_reserves_history: {
        title: 'Oljereservar etter funntiår',
        unit: 'Milliardar fat olje',
        group: 'funntiår',
        filename: '/data/cumulative net reserves oil gboe.csv',
        screenshot: 'reserves history oil gboe.png'
    },
    gas_reserves_history: {
        title: 'Gassreservar etter funntiår',
        unit: 'Milliardar fat oljeekvivalentar',
        group: 'funntiår',
        filename: '/data/cumulative net reserves gas gboe.csv',
        screenshot: 'reserves history gas gboe.png'
    },
    oe_reserves_history: {
        title: 'Petroleumreservar etter funntiår',
        unit: 'Milliardar fat oljeekvivalentar',
        group: 'funntiår',
        filename: '/data/cumulative net reserves oe gboe.csv',
        screenshot: 'reserves history oe gboe.png'
    },
};

var mode = findGetParameter('mode', 'oil');
show_resource(m[mode].title, m[mode].group, m[mode].unit, m[mode].filename);

// show_resource('oljeproduksjon', 'Millionar fat/dag', '/data/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
// show_resource('gassproduksjon', 'Millionar fat oljeekvivalentar/dag', '/data/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
// show_resource('petroleumproduksjon', 'Millionar fat oljeekvivalentar/dag', '/data/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv');
