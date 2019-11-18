from flask import Flask, render_template, request, escape, url_for, make_response, jsonify, session, redirect, flash

app = Flask(__name__)
app.secret_key = "find yours"

@app.route("/<firstname>/<lastname>")
def hellos(firstname, lastname):
    return f"Hello, let this be last time to do basics {firstname} {lastname}"

@app.route("/", methods=["POST", "GET"])
def home():
    #if request['firstname'] ==
    print(request.args.get("firstnam"))
    if request.method == "POST":
        try:
            print(request.form["mname"])
            print(request.cookies)
        except KeyError:
            print("that form attribute doesnt exist")
        flash("it worked")
    return render_template("index.html")

with app.test_request_context():
    print(url_for('home'))
    print(url_for('home'))
    print(url_for('home', next='/'))

@app.route("/emz")
def emz():
    resp = make_response(render_template('base.html'), 200)
    print(resp.headers['Content-Type'])
    return resp

@app.route('/api')
def api():
    return {
        "name" : "Emma",
        "age" : 30,
        "height" : "10fts"
    }

@app.route('/japi')
def japi():
    return jsonify({
        "name" : "Emma",
        "age" : 30,
        "height" : "10fts"
    })

@app.route('/login')
def login():
    if request.method == "POST":
        session['username'] = request.form["username"]
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))