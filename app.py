from flask import Flask,render_template,request

app=Flask(__name__)


@app.route('/')
def mainpage():
    print("server started")
    return render_template("index.html")