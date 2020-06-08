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
    """Returned te text miner pagina.
    :return: De pagina waarop kan worden gezocht met een gen of ziektetermen.
    """
    return render_template("text_miner.html")


@app.route('/contact')
def contact():
    """Returned te text miner pagina.
    :return: De pagina waarop kan worden gezocht met een gen of ziektetermen.
    """
    return render_template("contact.html")


@app.route('/textminer')
def textmined():
    """Returned te text miner pagina.
    :return: De pagina waarop kan worden gezocht met een gen of ziektetermen.
    """
    return render_template("text_miner.html")


@app.route('/resultaat', methods=['get', 'post'])
def result():
    """Deze functie roept de functies aan.
    :return:De resultaten pagina met een tabel met alle resultaten.
    """
    dict, zoekwoord, gen_or_disease = create_dict()
    gennamen = genpanel_inlezen()
    result = tabel(dict, zoekwoord, gennamen, gen_or_disease)
    return render_template("resultaat.html", resultaat=Markup(result))


def create_dict():
    """Verkijg de input van de gebruiker.
    Open het bestand en kijk of de zoekterm in het bestand voorkomt.
    Maak een dictionary met de artikelen als key waar de zoektermen in voorkomen.
    De values in de dictionary bestaan uit de gevonden genen.
    :return: Dictionary met gevonden artikelen en genen.
    De gebruikte zoektermen worden gereturned.
    Er wordt gereturned of er ziekte of gen door de gebruiker is ingevuld.
    """
    zoekwoord = request.form["woord"]       # Verkrijg de klinische zoekterm.
    zoekwoord = zoekwoord.lower()
    gen = request.form["gen"]       # Verkrijg de genen/het gen.
    gen_or_disease = 'Disease'
    with open("pmc_twee.json", 'r') as file:
        data = file.read()
    obj = json.loads(data)
    dict = {}
    g = get_gene_list(gen)
    genes = get_synonyms(g)     # Verkrijg synoniemen van genen.
    if g == ['']:
        gen_or_disease, dict = resulting(obj, zoekwoord, gen, gen_or_disease, dict)
    else:
        for gen in genes:       # Uitvoeren als er meerdere genen zijn ingevuld.
            gen_or_disease, dict = resulting(obj, zoekwoord, gen, gen_or_disease, dict)
    if gen_or_disease == 'Gene':
        zoekwoord = ','.join(g)
    return dict, zoekwoord, gen_or_disease


def resulting(obj, zoekwoord, gen, gen_or_disease, dict):
    """Voor elk artikel wordt er gekeken of de zoektermen
    overeenkomen met inhoud van het artikel.
    :param obj: Het bestand dat wordt gebruikt.
    :param zoekwoord: Het zoekwoord ingevuld door de gebruiker.
    :param gen: Het gen ingevuld door de gebruiker.
    :param gen_or_disease: Of de gebruiker een gen of een ziekte heeft ingevuld.
    :param dict: Bevat de PMC en de genen die zijn gevonden.
    :return: Of de gebruiker een gen of ziekte heeft ingevuld.
    :return: De dictionary met PMC en genen.
    """
    for article in obj:
        for item in article["Article"]:
            # Voer uit als ziekte is ingevuld, maar gen niet.
            if zoekwoord in item["diseases"] and gen == "":
                toevoegen_dict(item, dict)
            # Voer uit als zoekterm en gen zijn ingevuld.
            elif zoekwoord in item["diseases"] and gen != "":
                if gen.strip() in item["genes"]:
                    toevoegen_dict(item, dict)
            # Voer uit als zoekwoord leeg is, maar gen is ingevuld.
            elif zoekwoord == "" and gen.strip() in item["genes"]:
                toevoegen_dict(item, dict)
                gen_or_disease = 'Gene'
    return gen_or_disease, dict


def get_gene_list(gen):
    """Functie kijkt of er meerdere genen zijn ingevuld.
    De genen worden gescheiden op basis van komma's.
    :param gen: Gebruikt om te kijken of het uit meerdere genen bestaat.
    :return: Een lijst met de genen.
    """
    if ',' in gen:
        genes = gen.split(',')
    else:
        genes = [gen]
    return genes


def get_synonyms(genes):
    """Het bestand wordt geopend met genen en synoniemen.
    Voor de ingevoerde genen wordt gezocht naar de synoniemen.
    Indien het gen synoniemen bevat, wordt daar mee gezocht.
    :param genes: Gebruikt om te zoeken naar synoniemen.
    :return: Lijst met genen die worden gebruikt om te zoeken.
    """
    list_gene = []
    with open("gene.json", 'r') as file:
        data = file.read()
    obj = json.loads(data)
    for gene in genes:
        for value in obj:
            for k, v in value.items():
                for i in v:
                    if gene.strip() == i.strip():
                        list_gene = list_gene + v
    if len(list_gene) == 0:
        return genes
    return list_gene


def toevoegen_dict(item, dict):
    """Voeg PMC aan dictionary toe met bijbehorende genen.
    :param item: Daarvan worden de genen toegevoegd.
    :param dict: Gebruikt om de PMC en genen te bewaren.
    :return: Niks
    """
    try:
        if item["PMC"] in dict.keys():
            dict[item["PMC"]] += item["genes"]      # Update genen in dictionary.
            dict[item["PMC"]] = sorted(dict[item["PMC"]], key=str.casefold)
        else:
            dict[item["PMC"]] = item["genes"]       # Voeg genen toe aan dictionary.
            dict[item["PMC"]] = sorted(dict[item["PMC"]], key=str.casefold)

    except:
        print("exception")


def genpanel_inlezen():
    """Open bestand.
    Maak een lijst met alle genen uit het genpanelbestand.
    :return: Lijst met de gennamen uit genpanel.
    """
    file = open("GenPanels_merged_DG-2.17.0.txt")
    gennamen = []
    for regel in file:
        if regel.startswith("Symbol_HGNC"):
            print("Dit zijn alle genen: ")
        else:
            genpanel = regel.split("\t")
            gennaam = genpanel[0]       # Hier staat de gennaam.
            gennamen.append(gennaam)
    return gennamen


def tabel(dict, zoekwoord, gennamen, gene_or_disease):
    """Er wordt gekeken of de gevonden genen in genpanelbestand voorkomen.
    Er wordt een tabel gemaakt met de zoekterm, genen en pmc codes.    
    :param dict: Bevat de PMC codes en genen die zijn gevonden.
    :param zoekwoord: Wat de gebruiker heeft ingevuld.
    :param gennamen: Gebruikt om te kijken of het in het genpanel voorkomt.
    :param gene_or_disease: Of de gebruiker een gen of ziekte heeft ingevuld.
    :return: Een tabel met zoekterm, genen en pmc codes.
    """
    result = f"<table><tr><th>{gene_or_disease}</th><th>PMC code</th><th>Genes</th><th>Gevonden in genpanellijst</td></tr>"
    for key, values in dict.items():
        gevonden = find_in_genpanel(values, gennamen)
        try:
            filtered_values = filter_genes(values)
            result = result + "<tr><td>" + zoekwoord + "</td><td><a href='https://www.ncbi.nlm.nih.gov/pmc/articles/{}' target='_blank'>".format(key) + key +\
                     "</td><td>" + printer(filtered_values) + "</td><td>" + printer(gevonden) + "</td></tr>"
        except:
            gevonden = ""
            filtered_values = filter_genes(values)
            result = result + "<tr><td>" + zoekwoord + "</td><td>" + "</td><td><a href='https://www.ncbi.nlm.nih.gov/pmc/articles/{}' target='_blank'>".format(key) + key + \
                     "</td><td>" + printer(filtered_values) + "</td><td>" + printer(gevonden) + "</td></tr>"

    result = result + "</table>"
    return result


def find_in_genpanel(values, gennamen):
    """Kijkt of gevonden gen in genpanel staat.    
    :param values: Bevat de gevonden genen.
    :param gennamen: Bevat de genen uit genpanelbestand.
    :return: Een lijst met de genen die zijn gevonden,
    maar ook in het genpanelbestand staan.
    """
    gevonden = []
    for value in values:
        if value in gennamen:
            gevonden.append(value)
    return gevonden


def filter_genes(genes):
    """Bevat een lijst met woorden die geen genen zijn.
    De woorden worden gebruikt om false positive genen te verwijderen.
    :param genes: De gevonden genen.
    :return: Een lijst met genen die gefiltered is.
    """
    no_genes = ['receptor', 'protein', 'enzyme', 'enzym', 'hormone', 'insulin', 'antigen', 'ase', 'mir', 'rna']
    filtered_genes = []
    for gen in genes:
        if gen.count(' ') > 2:
            pass
        else:
            if not any(ext in gen.lower() for ext in no_genes):
                filtered_genes.append(gen)
    return filtered_genes


def printer(values):
    """Maakt een string van alle gevonden genen.
    :param values: De gevonden genen.
    :return: Een string van de gevonden genen.
    """
    string_builder = ''
    for i in values:
        string_builder = string_builder + i + ', '
    return string_builder[:-2]


if __name__ == '__main__':
    app.run(debug=True)

