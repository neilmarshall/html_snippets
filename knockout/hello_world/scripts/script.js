// declare + define view-model
function AppViewModel() {
  let self = this;

  self.firstName = ko.observable("Bert");
  self.lastName = ko.observable("Bertington");

  self.fullName = ko.computed(function() {
    return `${self.firstName()} ${self.lastName()}`;
  }, self);

  self.capitalizeLastName = function() {
    self.lastName(self.lastName().toUpperCase());
  };

  self.randomiseName = function() {
    let rnd = () => Math.floor(Math.random() * 10);
    let names = ['Andy', 'Ben', 'Carl', 'Dave', 'Eric', 'Fred', 'George', 'Harry', 'Ian', 'John'];
    self.firstName(names[rnd()]);
  };

  self.intToAdd = ko.observable("");
  self.intArray = ko.observableArray([1, 2, 3]);
  self.intPush = function() {
    self.intArray.push(self.intToAdd());
    self.intToAdd("");
  }
  self.intArrayTotal = ko.computed(() =>
    self.intArray().reduce((a, b) => a + parseInt(b), 0));
}

// bind view-model
let main = function() {
  ko.applyBindings(new AppViewModel());
}
