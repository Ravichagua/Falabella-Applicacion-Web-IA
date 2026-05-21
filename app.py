from flask import Flask,request,render_template # type: ignore

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/busqueda")
def busqueda():
    return render_template("busqueda.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)