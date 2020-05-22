from flask import Flask, render_template, request
from Bio import Entrez
from datetime import date
import re

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

@app.route('/textminer', methods=['post'])
def textmined():
    return render_template("text_miner.html")


@app.route('/resultaat', methods=['get', 'post'])
def result():
    zoekwoord = request.form["woord"]
    try:
        jaar = request.form["jaar"]
        jaar = jaar + '/01/01'
    except:
        jaar = "0/0/0"
    gezocht, aantal = zoeken(zoekwoord, jaar)
    id_lijst = gezocht['IdList']
    details = details_ophalen(id_lijst)
    samenvatting, abstracts = verkrijg_titel(details, zoekwoord)
    gen_uit_abstract(abstracts)
    return render_template("resultaat.html") + samenvatting

def zoeken(zoekwoord, jaar):
    vandaag = date.today()
    vandaag = str(vandaag).replace('-', '/')
    Entrez.email = 'example@mail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmode='xml',
                            retmax=30,
                            mindate=jaar,
                            maxdate=vandaag,
                            term=zoekwoord)
    results = Entrez.read(handle)
    #print(results)
    aantal = results['Count']
    return results, aantal

def details_ophalen(id_lijst):
    ids = ','.join(id_lijst)
    Entrez.email = 'example@mail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def verkrijg_titel(publicaties, zoekwoord):
    overzicht = "<table><tr><th>zoekwoord</th><th>publicatiedatum</th><th>artikeltitel pubmed</th></tr>"
    abstracts = ""
    for i, paper in enumerate(publicaties['PubmedArticle']):
        try:
            year = int(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year'])
            artikel = (paper['MedlineCitation']['Article']["ArticleTitle"])
            abstract = (paper['MedlineCitation']['Article']["Abstract"]["AbstractText"])
            overzicht = overzicht + "<tr><td>" + zoekwoord +"</td>" + "<td>" + str(year) + "</td><td>" + str(artikel)\
                        + "</td></tr>"
            abstracts = abstracts + str(abstract) + "\n"
        except:
            pass
    overzicht = overzicht + "</table>"
    return overzicht, abstracts


def gen_uit_abstract(abstracts):
    abstracts = abstracts.split('\n')
    for abstract in abstracts:
        abstract = abstract.split(' ')
        for word in abstract:
            gen = re.sub('[\W_]+', '', word)
            if len(gen) > 2 and len(gen) < 6 and not gen.startswith('p'):
                if gen.isalpha():
                    if gen.isupper():
                        print(gen)
                elif re.search(r'\d', word):
                    if not gen.isdigit():
                        print(gen)

@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
