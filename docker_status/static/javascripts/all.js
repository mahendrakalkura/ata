var application = angular.module('application', ['angular-loading-bar']);

application.config([
    '$compileProvider',
    '$interpolateProvider',
    'cfpLoadingBarProvider',
    function (
        $compileProvider,
        $interpolateProvider,
        cfpLoadingBarProvider
    ) {
        $compileProvider.debugInfoEnabled(false);

        // ...because {{ and }} is used by Django.
        $interpolateProvider.startSymbol('[!');
        $interpolateProvider.endSymbol('!]');

        // ...because it breaks the layout.
        cfpLoadingBarProvider.includeSpinner = false;
    }
]);

application.controller('controller', [
    '$attrs',
    '$element',
    '$http',
    '$scope',
    function ($attrs, $element, $http, $scope) {
        $scope.containers = [];
        $scope.spinner = true;

        $scope.refresh = function () {
            $scope.containers = [];
            $scope.spinner = true;
            $http({
                method: 'GET',
                url: $attrs.url,
            })
                .then(
                    function (response) {
                        $scope.containers = response.data;
                        $scope.spinner = false;
                    },
                    function () {
                        $scope.containers = [];
                        $scope.spinner = false;
                    }
                );
        };

        $scope.checkAll = function ($index) {
            angular.forEach($scope.containers, function (value, key) {
                $scope.check(key);
            });
        };

        $scope.check = function ($index) {
            $scope.containers[$index].spinner = true;
            $http({
                method: 'GET',
                url: $scope.containers[$index].urls.check,
            })
                .then(
                    function (response) {
                        $scope.containers[$index].new_version = (
                            response.data.new_version
                        );
                        $scope.containers[$index].spinner = false;
                    },
                    function () {
                        $scope.containers[$index].spinner = false;
                    }
                );
        };

        $scope.update = function ($index) {
            $scope.containers[$index].spinner = true;
            $http({
                method: 'POST',
                url: $scope.containers[$index].urls.update,
            })
                .then(
                    function (response) {
                        // ...success
                        // ...refresh the list in order to see the newly
                        // started containers
                        $scope.refresh();
                    },
                    function () {
                        // ...failure
                        // ...refresh the list in order to retry
                        $scope.refresh();
                    }
                );
        };

        $scope.refresh();
    }
]);
