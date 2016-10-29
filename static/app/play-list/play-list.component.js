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
                self.orderProp = '-date';
                PlayResource.query({ playId: '' }, function (plays) {
                    self.setPlays(plays);
                });

                self.setPlays = function setPlays(plays) {
                    self.plays = plays;
                };

                self.getDate = function getDate(play) {
                    // date in play is a timestamp
                    //convert it to date using Date constructor
                    return new Date(play.date).toISOString().slice(0, 10).replace(/-/g, "/");
                };

                /**
                 * Return the id of the given play
                 */
                self.getPlayId = function getPlayId(play) {
                    return play._id['$oid'];
                };
            }]
    });
