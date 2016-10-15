'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
  module('playList').
  component('playListComponent', {
    templateUrl: 'static/app/play-list/play-list.template.html',
    controller: ['PlayResource',
      function PlayListController(PlayResource) {
        var self = this;
        self.plays = [];
        self.orderProp = '-id';
        PlayResource.query({playId:''}, function(plays){
          self.setPlays(plays);
        });

        self.setPlays = function setPlays(plays){
          self.plays = plays;
        };
      }]
  });
