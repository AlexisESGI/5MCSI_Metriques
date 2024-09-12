from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
@app.route('/api/commits/')
def commits():
    # Récupération des données des commits depuis l'API GitHub
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    # Compter les commits par minute
    minutes_count = {}
    for commit in json_content:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        if minute in minutes_count:
            minutes_count[minute] += 1
        else:
            minutes_count[minute] = 1
    
    return jsonify(minutes_count)

@app.route('/commits/')
def commits_graph():
    # Servir le fichier HTML pour le graphique
    return render_template('commits.html')


if __name__ == "__main__":
  app.run(debug=True)

