$(function() {
    let viewModel = function() {
        let getResponseAsync = function(input, output, route) {
            if (input()) {
                $.get(route, function(data, status) {
                    if (status === "success") {
                        console.log(data);
                        output(data);
                    } else {
                        console.log("something went wrong...");
                    }
                });
            }
        };

        let self = this;

        self.numberToCheckInput = ko.observable(null);
        self.numberToCheckOutput = ko.observable(null);
        self.numberToCheckBinder = ko.computed(function() { getResponseAsync(
            self.numberToCheckInput,
            self.numberToCheckOutput,
            `/api/is-prime/${self.numberToCheckInput()}`);
        });

        self.numberToFactoriseInput = ko.observable(null);
        self.numberToFactoriseOutput = ko.observable(null);
        self.numberToFactoriseBinder = ko.computed(function() { getResponseAsync(
            self.numberToFactoriseInput,
            self.numberToFactoriseOutput,
            `/api/get-factors/${self.numberToFactoriseInput()}`);
        });
    };

    ko.applyBindings(viewModel);
});
