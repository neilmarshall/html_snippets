import json
from flaskr import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    form = BrandModelSelector()
    return render_template('index.html', form=form)


class BrandModelSelector():

    brands = ["Audi", "BMW", "Citroen"]

    models = {"Audi": ["A3", "A5", "Q5", "Q7"],
               "BMW": ["1 Series", "3 Series", "5 Series", "X1", "X3", "X5"],
               "Citroen": ["C1", "C2", "C3", "C4", "C5", "C6", "C8"]}

    @property
    def brandsJSON(self):
        return json.dumps(self.brands)

    @property
    def modelsJSON(self):
        return json.dumps(self.models)
