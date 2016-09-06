'use strict';

angular.
  module('phonecatApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');
      $routeProvider.
        when('/plays', {
          template: '<play-list></play-list>'
        }).
        when('/plays/:playId', {
          template: '<play-detail></play-detail>'
        }).
        otherwise('/plays');
    }
  ]);
