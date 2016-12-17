'use strict';

angular.
    module('playList').
    component('playListComponent', {
        templateUrl: 'static/app/play-list/play-list.template.html',
        controller: ['PlayResource', 'AuthCommon', '$http',
            function PlayListController(PlayResource, AuthCommon, $http) {
                var self = this;
                self.auth = AuthCommon;
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
                    if(play._id){
                        return play._id['$oid'];
                    }
                    return undefined;
                };
            }]
    });
