from flask import Flask, render_template, request, Markup
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
    dict, zoekwoord = create_dict()
    result = tabel(dict, zoekwoord)
    return render_template("resultaat.html", resultaat=Markup(result))


def create_dict():
    zoekwoord = request.form["woord"]
    zoekwoord = zoekwoord.lower()
    with open("data.json", 'r') as file:
        data = file.read()
    obj = json.loads(data)
    dict = {}
    for article in obj:
        for item in article["Article"]:
            if zoekwoord in item["diseases"]:
                try:
                    if item["PMC"] in dict.keys():
                        dict[item["PMC"]] += item["genes"]
                    else:
                        dict[item["PMC"]] = item["genes"]
                except:
                    print("exception")
    return dict, zoekwoord

def tabel(dict, zoekwoord):
    result = "<table><tr><th>searchterm</th><th>PMC code</th><th>Genes</th></tr>"
    for key,values in dict.items():
        result = result + "<tr><td>" + zoekwoord + "</td><td>" + key + "</td><td>" + str(values) + "</td></tr>"

    # result = result + "<tr><td>" + zoekwoord + "</td><td>" + item["PMC"] + "</td><td>" + str(item["genes"]) + "</td></tr>"
    result = result + "</table>"
    return result



@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
