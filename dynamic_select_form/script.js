window.onload = main;

function main()  {
    load_brands();
}

function load_brands() {
    var select = document.getElementById("brands");
    var brands = ["Audi", "BMW", "Citroen"];
    brands.forEach(function(brand) {
        select.options.add(Option(brand));
    });
    load_models();
}

function load_models() {
    var select = document.getElementById("models");
    select.options.length = 0;
    var models_by_brand = {
        "Audi": ["A3", "A5", "Q5", "Q7"],
        "BMW": ["1 Series", "3 Series", "5 Series", "X1", "X3", "X5"],
        "Citroen": ["C1", "C2", "C3", "C4", "C5", "C6", "C8"]
    };
    var brand = document.getElementById("brands");
    var models = models_by_brand[brand.value];
    models.forEach(function(model) {
        select.options.add(Option(model));
    });
}
