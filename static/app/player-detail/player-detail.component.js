'use strict';

angular.
  module('playerDetail').
  component('playerDetailComponent', {
    bindings: { playerId: '<' },
    templateUrl: 'static/app/player-detail/player-detail.template.html',
    controller: ['PlayerResource',
      function PlayerDetailController(PlayerResource) {
        var self = this;
        PlayerResource.get({playerId: self.playerId}, function(player) {
          self.setPlayer(player);
        });

        self.setPlayer = function setPlayer(player) {
          self.player = player;
        };
      }
    ]
  });
