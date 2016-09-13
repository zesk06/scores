'use strict';

// Register `playDetail` component, along with its associated controller and template
angular.
  module('playDetail').
  component('playDetailComponent', {
    bindings: { playId: '<' },
    templateUrl: 'static/app/play-detail/play-detail.template.html',
    controller: ['PlayResource',
      function PhoneDetailController(PlayResource) {
        var self = this;
        PlayResource.get({ playId: self.playId }, function (play) {
          self.setPlay(play);
        });

        self.setPlay = function setPlay(play) {
          self.play = play;
        };
      }
    ]
  });
