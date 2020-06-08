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
    dict, zoekwoord, gen_or_disease = create_dict()
    gennamen = genpanel_inlezen()
    result = tabel(dict, zoekwoord, gennamen, gen_or_disease)
    return render_template("resultaat.html", resultaat=Markup(result))


def create_dict():
    zoekwoord = request.form["woord"]
    zoekwoord = zoekwoord.lower()
    gen = request.form["gen"]
    gen_or_disease = 'Disease'
    with open("pmc_twee.json", 'r') as file:
        data = file.read()
    obj = json.loads(data)
    dict = {}
    for article in obj:
        for item in article["Article"]:
            if zoekwoord in item["diseases"] and gen == "":
               toevoegen_dict(item, dict)
            elif zoekwoord in item["diseases"] and gen != "":
                if request.form["gen"] in item["genes"]:
                    toevoegen_dict(item, dict)
            elif zoekwoord == "" and gen in item["genes"]:
                toevoegen_dict(item, dict)
                gen_or_disease = 'Gene'

    if gen_or_disease == 'Gene':
        zoekwoord = gen

    return dict, zoekwoord, gen_or_disease


def toevoegen_dict(item, dict):
    try:
        if item["PMC"] in dict.keys():
            dict[item["PMC"]] += item["genes"]
        else:
            dict[item["PMC"]] = item["genes"]
    except:
        print("exception")

def genpanel_inlezen():
    file = open("GenPanels_merged_DG-2.17.0.txt")
    gennamen = []
    for regel in file:
        if regel.startswith("Symbol_HGNC"):
            print("Dit zijn alle genen: ")
        else:
            genpanel = regel.split("\t")
            gennaam = genpanel[0]
            gennamen.append(gennaam)
    return gennamen


def tabel(dict, zoekwoord, gennamen, gene_or_disease):
    result = f"<table><tr><th>{gene_or_disease}</th><th>PMC code</th><th>Genes</th><th>Gevonden in genpanellijst</td></tr>"
    for key, values in dict.items():
        gevonden = find_in_genpanel(values, gennamen)
        try:
            result = result + "<tr><td>" + zoekwoord + "</td><td><a href='https://www.ncbi.nlm.nih.gov/pmc/articles/{}' target='_blank'>".format(key) + key +\
                     "</td><td>" + printer(values) + "</td><td>" + printer(gevonden) + "</td></tr>"
        except:
            gevonden = ""
            result = result + "<tr><td>" + zoekwoord + "</td><td>" + "</td><td><a href='https://www.ncbi.nlm.nih.gov/pmc/articles/{}' target='_blank'>".format(key) + key + \
                     "</td><td>" + printer(values) + "</td><td>" + printer(gevonden) + "</td></tr>"


    result = result + "</table>"
    return result


def find_in_genpanel(values, gennamen):
    gevonden = []
    for value in values:
        print(value)
        print(values)
        if value in gennamen:
            gevonden.append(value)
    return gevonden


def printer(values):
    string_builder = ''
    for i in values:
        string_builder = string_builder + i + ', '
    return string_builder[:-2]


@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
