(function () {
    'use strict';

    angular.module('tree.directives')
        .directive('d3Bars', ['d3', function (d3) {
            return {
                restrict: 'EA',
                scope: {
                    data: "="
                },
                link: function (scope, iElement, iAttrs) {

                    var width = 900,
                        height = 600;

                    var cluster = d3.layout.cluster()
                        .size([height, width - 160]);

                    var diagonal = d3.svg.diagonal()
                        .projection(function (d) {
                            return [d.y, d.x];
                        });

                    var svg = d3.select(iElement[0]).append("svg")
                        .attr("width", width)
                        .attr("height", height)
                        .append("g")
                        .attr("transform", "translate(60,0)");

                    //.attr("width", "100%");

                    // on window resize, re-render d3 canvas
                    window.onresize = function () {
                        return scope.$apply();
                    };
                    scope.$watch(function () {
                            return angular.element(window)[0].innerWidth;
                        }, function () {
                            return scope.render(scope.data);
                        }
                    );

                    // watch for data changes and re-render
                    scope.$watch('data', function (newVals, oldVals) {
                        return scope.render(newVals);
                    }, false);

                    // define render function
                    scope.render = function (data) {
                        // remove all previous items before render
                        svg.selectAll("*").remove();

                        var nodes = cluster.nodes(data),
                            links = cluster.links(nodes);

                        var link = svg.selectAll(".link")
                            .data(links)
                            .enter().append("g");
                            //.attr("class", "link");

                        link.append("path")
                            .attr("class", "link")
                            .attr("d", diagonal);

                        link.append("text")
                            .attr("x", function(d) { return (d.source.y + d.target.y) / 2; })
                            .attr("y", function(d) { return (d.source.x + d.target.x) / 2; })
                            .attr("text-anchor", "middle")
                            .attr("class", "linktext")
                            .text(function(d) {

                                if (d.target.name.slice(-1) == 'L') {
                                    if (d.source.var_type == 'linear') {
                                        return '< ' + d.source.var_limits[1];
                                    }
                                    else if (d.source.var_type == 'circular') {
                                        return '[' + d.source.var_limits[0] + ', ' + d.source.var_limits[1] + ')';
                                    }
                                    else if (d.source.var_type == 'date' || d.source.var_type == 'time') {
                                        return d.source.var_limits[0] + ' / ' + d.source.var_limits[1];
                                    }
                                }
                                else if (d.target.name.slice(-1) == 'R') {
                                    if (d.source.var_type == 'linear') {
                                        return '> ' + d.source.var_limits[2];
                                    }
                                    else if (d.source.var_type == 'circular') {
                                        return '[' + d.source.var_limits[2] + ', ' + d.source.var_limits[3] + ')';
                                    }
                                    else if (d.source.var_type == 'date' || d.source.var_type == 'time') {
                                        return d.source.var_limits[2] + ' / ' + d.source.var_limits[3];
                                    }
                                }
                            });

                        var node = svg.selectAll(".node")
                            .data(nodes)
                            .enter().append("g")
                            .attr("class", "node")
                            .attr("transform", function (d) {
                                return "translate(" + d.y + "," + d.x + ")";
                            })

                        node.append("circle")
                            .attr("r", 4.5);

                        node.append("text")
                            .attr("dx", function (d) {
                                return d.children ? -8 : 8;
                            })
                            .attr("dy", 3)
                            .style("text-anchor", function (d) {
                                return d.children ? "end" : "start";
                            })
                            .text(function (d) {
                                return d.children ? d.var_name : d.value;
                            });

                    };
                }
            };
        }]);

}());
