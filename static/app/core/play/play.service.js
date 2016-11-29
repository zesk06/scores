'use strict';

angular.
  module('core.play').
  factory('PlayResource', ['$resource',
    // see $resource documentation:
    // https://docs.angularjs.org/api/ngResource/service/$resource
    function($resource) {
      return $resource('api/v1/plays/:playId');
    }
  ]);
