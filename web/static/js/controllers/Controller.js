var app = angular.module('tree.controllers', [])

app.controller('ContactController', function ($scope, $http) {

    $scope.bin_value = 50

    $scope.busy = false

    $http.get("datasets").success(function (data) {
        $scope.datasets = data;
    }).error(function () {
        alert("Unexpected error!")
    });

    $scope.selectDataset = function () {
        $http.get("datasets/" + $scope.dataset).success(function (data) {
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
        data_out = {}
        data_out["min_leaf"] = $scope.bin_value
        data_out["variables"] = $scope.variables
        $scope.busy = true
        $http({
            url: 'http://188.226.143.52:80/datasets/' + $scope.dataset,
            method: "POST",
            data: data_out,
            headers: {'Content-Type': 'text/javascript'}
        }).success(function (data, status, headers, config) {
            $scope.d3Data = data
            $scope.busy = false
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