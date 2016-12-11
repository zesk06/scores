'use strict';

angular.
    module('playList').
    component('playListComponent', {
        templateUrl: 'static/app/play-list/play-list.template.html',
        controller: ['PlayResource', '$http',
            function PlayListController(PlayResource, $http) {
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
                    if(play._id){
                        return play._id['$oid'];
                    }
                    return undefined;
                };

                self.isLogged = function(){
                    return document.user_is_logged;
                };

                self.deleteModal = function(play){
                    // ask to confirm such an operation
                    if(play){
                        self.delete_modal_play = play;
                    }
                    $('#myModal').modal();
                    return;
                };

                self.delete = function(play){
                    //send DELETE request you fool
                    console.log('DELETE ', play);
                    self.delete_modal_play = undefined;
                    var req = {
                        method: 'DELETE',
                        url: '/api/v1/plays/'+self.getPlayId(play),
                    };
                    $http(req).then(
                        function(response){
                            console.log('delete successfull', response);
                            $('#myModal').modal('hide');
                            self.removePlay(self.getPlayId(play));
                        },
                        function(response){
                            console.log('delete failed', response);
                            $('#myModal').modal('hide');
                        }
                    );
                };

                self.removePlay = function(playId){
                    for(var playIndex in self.plays){
                        var play = self.plays[playIndex];
                        if(self.getPlayId(play) === playId){
                            self.plays.splice(playIndex, 1);
                        }
                    }
                };
            }]
    });
