from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)

app.secret_key = '0ksklf8rfsks'

@app.route("/success")
def success():
    flash("Your operation was successful!", "success")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")
