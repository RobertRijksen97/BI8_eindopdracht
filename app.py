from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def homepage():
    """Deze functie runt de app
    :return: homepagina met informatie over de website
    """
    return render_template('home.html')


@app.route('/textminer')
def textminer():
    return render_template("text_miner.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/textminer', methods=['post'])
def textmined():
    return render_template("text_miner.html")


@app.route('/resultaat', methods=['get', 'post'])
def result():
    result = "<table><tr><th>searchterm</th><th>PMC code</th><th>Genes</th></tr>"
    zoekwoord = request.form["woord"]
    zoekwoord = zoekwoord.lower()
    with open("data.json",  'r') as file:
        data = file.read()
    obj = json.loads(data)
    for article in obj:
        for item in article["Article"]:
            if zoekwoord in item["diseases"]:
                result = result + "<tr><td>" + zoekwoord + "</td><tr>" + item["PMC"] + "</td><td>" + str(item["genes"]) + "</td></tr>"
    result = result + "</table>"
    return render_template("resultaat.html") + result + "<div id='footer'><img class='rad-logo' src='../static/img/Radboudumc-logo.jpg'>" \
                                                        "</div></body></html>"


@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
