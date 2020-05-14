from flask import Flask, render_template, request
from Bio import Entrez

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
    #print(request)
    zoekwoord = request.form["woord"]
    gezocht, aantal = zoeken(zoekwoord)
    id_lijst = gezocht['IdList']
    details = details_ophalen(id_lijst)
    samenvatting = verkrijg_titel(details, zoekwoord)
    return render_template("resultaat.html") + samenvatting

def zoeken(zoekwoord):
    Entrez.email = 'example@mail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmode='xml',
                            retmax=10,
                            term=zoekwoord)
    results = Entrez.read(handle)
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
    for i, paper in enumerate(publicaties['PubmedArticle']):
        try:
            year = int(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year'])
            artikel = (paper['MedlineCitation']['Article']["ArticleTitle"])
            overzicht = overzicht + "<tr><td>" + zoekwoord +"</td>" + "<td>" + str(year) + "</td><td>" + str(artikel)\
                        + "</td></tr>"
        except:
            pass
    print(overzicht)
    overzicht = overzicht + "</table>"
    return overzicht

@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
