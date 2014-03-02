(function () {
    'use strict';

    angular.module('tree.directives')
        .directive('d3Bars', ['d3', function (d3) {
            return {
                restrict: 'EA',
                scope: {
                    data: "=",
                    label: "@",
                    onClick: "&"
                },
                link: function (scope, iElement, iAttrs) {
                    console.log(iElement)
                    console.log(iElement[0])
                    var svg = d3.select(iElement[0])
                        .append("svg")
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
                    }, true);

                    // define render function
                    scope.render = function (data) {
                        // remove all previous items before render
                        svg.selectAll("*").remove();

                        var width = 800,
                            height = 600;

                        var cluster = d3.layout.cluster()
                            .size([height, width - 160]);

                        var diagonal = d3.svg.diagonal()
                            .projection(function (d) {
                                return [d.y, d.x];
                            });


                        function myFunction(my_data) {
                            var nodes = cluster.nodes(my_data),
                                links = cluster.links(nodes);

                            var link = svg.selectAll(".link")
                                .data(links)
                                .enter().append("path")
                                .attr("class", "link")
                                .attr("d", diagonal);

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
                                    return d.name;
                                });
                        };
                        myFunction(data)

                        d3.select(self.frameElement).style("height", height + "px");


                    };
                }
            };
        }]);

}());
