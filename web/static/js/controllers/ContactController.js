var app = angular.module('tree.controllers', [])

app.controller('ContactController', function ($scope, $http) {

    $http.get("datasets").success(function (data) {
        console.log(data)
        $scope.datasets = data;
    }).error(function () {
        alert("Unexpected error!")
    });

    $scope.selectDataset = function () {
        $http.get("datasets/" + $scope.dataset).success(function (data) {
            $scope.variables = data;
            $scope.var_name = $scope.variables[0].var_name;
        }).error(function () {
            alert("Unexpected error!")
        });
    };

    $scope.check_class = function (class_var) {
        console.log(class_var)
        var arrayLength = $scope.variables.length;
        for (var i = 0; i < arrayLength; i++) {
            if ($scope.variables[i]["var_name"] != class_var) {
                $scope.variables[i]["class_var"] = false;
            }
        }
    };

    $scope.getTree = function () {
        $http({
            url: 'http://127.0.0.1:5000/datasets/' + $scope.dataset,
            method: "POST",
            data: $scope.variables,
            headers: {'Content-Type': 'text/javascript'}
        }).success(function (data, status, headers, config) {
            console.log(data);
            $scope.d3Data = data
        }).error(function (data, status, headers, config) {
            console.log(status);
        });
    };

    $scope.title = "DemoCtrl";

    $scope.d3Data = {
        "name": "O",
        "children": [
            {
                "value": 0.3888888888888889,
                "name": "OLx",
                "members": 198
            },
            {
                "name": "OR",
                "children": [
                    {
                        "name": "ORL",
                        "children": [
                            {
                                "name": "ORLL",
                                "children": [
                                    {
                                        "value": 5.75,
                                        "name": "ORLLLx",
                                        "members": 28
                                    },
                                    {
                                        "value": 2.945945945945946,
                                        "name": "ORLLRx",
                                        "members": 37
                                    }
                                ]
                            },
                            {
                                "name": "ORLR",
                                "children": [
                                    {
                                        "name": "ORLRL",
                                        "children": [
                                            {
                                                "value": 9.708333333333334,
                                                "name": "ORLRLLx",
                                                "members": 24
                                            },
                                            {
                                                "name": "ORLRLR",
                                                "children": [
                                                    {
                                                        "name": "ORLRLRL",
                                                        "children": [
                                                            {
                                                                "value": 3.933333333333333,
                                                                "name": "ORLRLRLLx",
                                                                "members": 15
                                                            },
                                                            {
                                                                "name": "ORLRLRLR",
                                                                "children": [
                                                                    {
                                                                        "value": 8.380952380952381,
                                                                        "name": "ORLRLRLRLx",
                                                                        "members": 21
                                                                    },
                                                                    {
                                                                        "value": 6.057142857142857,
                                                                        "name": "ORLRLRLRRx",
                                                                        "members": 35
                                                                    }
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "value": 10.5,
                                                        "name": "ORLRLRRx",
                                                        "members": 12
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "name": "ORLRR",
                                        "children": [
                                            {
                                                "value": 3.967741935483871,
                                                "name": "ORLRRLx",
                                                "members": 31
                                            },
                                            {
                                                "name": "ORLRRR",
                                                "children": [
                                                    {
                                                        "value": 7.589743589743589,
                                                        "name": "ORLRRRLx",
                                                        "members": 39
                                                    },
                                                    {
                                                        "value": 4.7272727272727275,
                                                        "name": "ORLRRRRx",
                                                        "members": 22
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "ORR",
                        "children": [
                            {
                                "value": 13.518518518518519,
                                "name": "ORRLx",
                                "members": 27
                            },
                            {
                                "name": "ORRR",
                                "children": [
                                    {
                                        "value": 8.709677419354838,
                                        "name": "ORRRLx",
                                        "members": 31
                                    },
                                    {
                                        "value": 6.285714285714286,
                                        "name": "ORRRRx",
                                        "members": 28
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    };
    $scope.d3OnClick = function (item) {
        alert(item.name);
    };

});