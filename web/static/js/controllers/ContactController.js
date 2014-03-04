var app = angular.module('tree.controllers', [])

app.controller('ContactController', function ($scope, $http) {

    $scope.bin_value = 50

    $http.get("datasets").success(function (data) {
        $scope.datasets = data;
    }).error(function () {
        alert("Unexpected error!")
    });

    $scope.selectDataset = function () {
        $http.get("datasets/" + $scope.dataset).success(function (data) {
            console.log(data)
            $scope.variables = data.descriptor;
            $scope.rows = data.rows;
            $scope.head = data.head;
            console.log(data.descriptor)
            $scope.var_name = $scope.variables[0].var_name;

        }).error(function () {
            alert("Unexpected error!")
        });
    };

    $scope.check_class = function (class_var) {
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
            $scope.d3Data = data
        }).error(function (data, status, headers, config) {
            console.log(status);
        });
    };

    $scope.d3Data = {
        "name": "O",
        "children": [
        ]
    };

});