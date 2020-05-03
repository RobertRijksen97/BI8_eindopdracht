from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def homepage():
    """Deze functie runt de app
    :return: homepagina met informatie over de website
    """
    return render_template('home.html')


@app.route('/textminer', methods=['get', 'post'])
def textminer():
    return render_template("text_miner.html")


@app.route('/resultaat', methods=['get', 'post'])
def result():
    return render_template("resultaat.html")


@app.route('/parameters', methods=['get', 'post'])
def parameters():
    return render_template("parameters.html")


if __name__ == '__main__':
    app.run(debug=True)
