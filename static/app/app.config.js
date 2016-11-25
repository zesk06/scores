'use strict';

angular.
  module('scoresApp').
  config(function ($stateProvider) {
    $stateProvider.state({
      name: 'index',
      url: '',
      component: 'playListComponent'
    });
    $stateProvider.state({
      name: 'plays',
      url: '/plays',
      component: 'playListComponent'
    });
    //player list
    $stateProvider.state({
      name: 'players',
      url: '/players',
      component: 'playerListComponent'
    });
    //play new '/plays/new'
    $stateProvider.state({
      name: 'play-new',
      url: '/plays/new',
      component: 'playNewComponent'
    });
    //play detail '/plays/{playId}'
    $stateProvider.state({
      name: 'play-detail',
      url: '/plays/{playId}',
      component: 'playDetailComponent',
      resolve: {
        playId: function ($transition$) {
          return $transition$.params().playId;
        }
      }
    });
    //player detail '/player/{playerId}'
    $stateProvider.state({
      name: 'player-detail',
      url: '/players/{playerId}',
      component: 'playerDetailComponent',
      resolve: {
        playerId: function ($transition$) {
          return $transition$.params().playerId;
        }
      }
    });
    //game detail '/game/{gameId}'
    $stateProvider.state({
      name: 'game-detail',
      url: '/games/{gameId}',
      component: 'gameDetailComponent',
      resolve: {
        gameId: function ($transition$) {
          return $transition$.params().gameId;
        }
      }
    });
  });




    // ['$stateProvider' ,'$routeProvider',
    // function config($locationProvider, $routeProvider) {
    //   $locationProvider.hashPrefix('!');
    //   $routeProvider.
    //     when('/plays', {
    //       template: '<play-list></play-list>'
    //     }).
    //     when('/plays/:playId', {
    //       template: '<play-detail></play-detail>'
    //     }).
    //     when('/games/:gameId', {
    //       template: '<game-detail></game-detail>'
    //     }).
    //     otherwise('/plays').
    //     when('/players/:playerId', {
    //       template: '<player-detail></player-detail>'
    //     }).
    //     otherwise('/plays');
    // }
    // ]);
