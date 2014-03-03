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

    /*
    $scope.d3Data = [
        {name: "Greg", score:98},
        {name: "Ari", score:96},
        {name: "Loser", score: 48}
    ];

    $scope.d3Data = [
        {"name": "A", "value":-15},
        {"name": "B", "value":-20},
        {"name": "C", "value":-5},
        {"name": "D", "value":5},
        {"name": "E", "value":15},
        {"name": "F", "value":25}
    ];*/


    $scope.d3Data = {
        "name": "O",
        "children": [
            {
                "value": 0.3888888888888889,
                "name": "OLx",
                "members": 198
            },
            {
                "value": 2.945945945945946,
                "name": "ORLLRx",
                "members": 37
            }
        ]
    };
    $scope.d3OnClick = function (item) {
        alert(item.name);
    };

});