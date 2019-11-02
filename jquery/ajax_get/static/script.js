$(function() {
    let viewModel = function() {
        let getResponseAsync = function(input, output, route) {
            if (input()) { $.get(route, output); }
        };

        let self = this;

        self.numberToCheckInput = ko.observable(null);
        self.numberToCheckOutput = ko.observable(null);
        ko.computed(function() {
            getResponseAsync(
                self.numberToCheckInput,
                self.numberToCheckOutput,
                `/api/is-prime/${self.numberToCheckInput()}`);
        });

        self.numberToFactoriseInput = ko.observable(null);
        self.numberToFactoriseOutput = ko.observable(null);
        ko.computed(function() {
            getResponseAsync(
                self.numberToFactoriseInput,
                self.numberToFactoriseOutput,
                `/api/get-factors/${self.numberToFactoriseInput()}`);
        });

        self.primeGeneratorLimit = ko.observable(null);
        self.generatedPrimes = ko.observable(null);
        ko.computed(function() {
            getResponseAsync(
                self.primeGeneratorLimit,
                self.generatedPrimes,
                `/api/get-primes/${self.primeGeneratorLimit()}`);
        });

        for (let button of document.querySelectorAll("button")) {
            let observable = button.dataset.observable;
            if (observable) {
                button.addEventListener('click', function() {
                    self[observable](null);
                });
            };
        }
    };

    ko.applyBindings(viewModel);
});
