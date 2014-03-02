(function () {
  'use strict';

  // create the angular app
  angular.module('tree', [
    'tree.controllers',
    'tree.directives'
    ]);

  // setup dependency injection
  angular.module('d3', []);
  angular.module('tree.controllers', []);
  angular.module('tree.directives', ['d3']);


}());