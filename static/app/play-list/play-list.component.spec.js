// jshint esversion: 6
'use strict';

describe('playList', function () {

    //load the module
    beforeEach(module('playList'));

    // Test the controller
    describe('PlayListControllerTest', function () {
        var $httpBackend, ctrl;

        var plays = [
            {
                "date": "01/09/15",
                "game": "7wonders",
                "id": 0,
                "players": [
                    {
                        "name": "lolo",
                        "score": 28
                    },
                    {
                        "name": "clemence",
                        "score": 46
                    },
                ]
            },
            {
                "date": "02/09/15",
                "game": "7wonders",
                "id": 1,
                "players": [
                    {
                        "name": "lolo",
                        "score": 39
                    },
                    {
                        "name": "clemence",
                        "score": 39
                    }
                ]
            }
        ];

        beforeEach(inject(function ($componentController, _$httpBackend_) {
            $httpBackend = _$httpBackend_;
            // program response
            $httpBackend.expectGET('/api/v1/plays')
                .respond(plays);
            //create controller here
            ctrl = $componentController('playListComponent');
        }));
        // Test
        it('should create a `plays` property with 2 plays fetched with `$http`', function () {
            jasmine.addCustomEqualityTester(angular.equals);
            expect(ctrl.plays).toEqual([]);
            $httpBackend.flush();
            expect(ctrl.plays.length).toBe(2);
            expect(ctrl.plays).toEqual(plays);
        });
        // Test
        it('should set a default value for the `orderProp` property', function () {
            expect(ctrl.orderProp).toBe('-date');
        });

    });

});
