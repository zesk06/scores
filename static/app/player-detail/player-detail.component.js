'use strict';

angular.
  module('playerDetail').
  component('playerDetail', {
    templateUrl: 'static/app/player-detail/player-detail.template.html',
    controller: ['$routeParams', 'PlayerResource',
      function PlayerDetailController($routeParams, PlayerResource) {
        var self = this;

        PlayerResource.get({playerId: $routeParams.playerId}, function(player) {
          self.setPlayer(player);
        });

        self.setPlayer = function setPlayer(player) {
          console.log(player);
          self.player = player;
        };
      }
    ]
  });
