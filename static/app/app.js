function myAppController($scope, testHttp) {
  $scope.plays = [];
  $scope.setPlays = function(playsArray){
    $scope.plays = playsArray;
  };

  testHttp.getPlays().then(function successCallback(response) {
            // this callback will be called asynchronously
            // when the response is available
            console.log('response received!')
            if(response.status === 200){
                console.log(response);
                $scope.setPlays(response.data);
            }else{
                console.log('Failed to retrieve datas');
            }
            //$scope.setPlays(response);
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log('an error occured '+response);
          });;

};

function testHttp($http){
    this.getPlays = function(){
        console.log('retrieving plays from http')
        // Simple GET request example:
        return $http.get('http://localhost:5000/api/v1/plays');
    }
};

angular.module('myApp', [])
       .service('testHttp', testHttp)
       .controller('myAppController', myAppController);
