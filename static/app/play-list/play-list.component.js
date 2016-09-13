'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
  module('playList').
  component('playListComponent', {
    templateUrl: 'static/app/play-list/play-list.template.html',
    controller: ['PlayResource',
      function PlayListController(PlayResource) {
        var self = this;
        PlayResource.query({playId:''}, function(plays){
          self.setPlays(plays);
        });
        this.orderProp = 'date';

        this.setPlays = function setPlays(plays){
          this.plays = plays;
        };
      }]
  });
