from flask import abort, Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-factors/<int:n>')
def get_factors(n):
    if n <= 0:
        abort(400, "argument must be a positive integer")
    if n == 1:
        return {'factors': [1]}
    factors = []
    for p in range(2, int(n**0.5) + 1):
        while n % p == 0:
            factors.append(p)
            n /= p
    if n != 1:
        factors.append(n)
    return {'factors': factors}

@app.route('/api/is-prime/<int:n>')
def is_prime(n):
    if n <= 0:
        abort(400, "argument must be a positive integer")
    if n in {1, 2}:
        return {'response': False if n == 1 else True}
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            return {'response': False}
    else:
        return {'response': True}
