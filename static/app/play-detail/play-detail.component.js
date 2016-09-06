'use strict';

// Register `playDetail` component, along with its associated controller and template
angular.
  module('playDetail').
  component('playDetail', {
    templateUrl: 'static/app/play-detail/play-detail.template.html',
    controller: ['$routeParams', 'PlayResource',
      function PhoneDetailController($routeParams, PlayResource) {
        var self = this;
        PlayResource.get({playId: $routeParams.playId}, function(play) {
          self.setPlay(play);
        });

        self.setPlay = function setPlay(play) {
          self.play = play;
        };
      }
    ]
  });
