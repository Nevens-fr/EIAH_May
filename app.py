# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

import getDataIndicateur as gDI
import json

app = Dash(__name__)

jsonopen=open("traceforum.json", "r")
f = json.load(jsonopen)


listeUser= gDI.listeUstilisateur(f["transition"])
dicoUser=gDI.creationDicoUser(listeUser)
dicoUser=gDI.calculNbConnexionNbMsgPoste(dicoUser,f["transition"])
dicoEleve,dicoEnseignant, dicoInactif = gDI.separationEleveEnseignant(dicoUser,listeUser,f["transition"])

jsonopen.close()

df = pd.DataFrame(dicoEleve)
print(df.to_json())

fig = px.bar(df, x="gdp per capita", y="life expectancy",color="continent", barmode="group")

eleves = []

for cle,valeur in dicoEleve.items():
    eleves.append(cle.replace("'",""))


#création de la mise en page
app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash'
    ),

    html.Div(children="Choissez un élève pour lequel vous souhaitez visualiser des indicateurs"),

    dcc.Dropdown(
        eleves,
        eleves[0],
        id="choix"
    ),

    html.Br(),

    html.Div([
        html.Label(children="Nombre de connexions : "),
        html.Label(id="nbCo")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Label(children="Nombre de messages postés : "),
        html.Label(id="nbMessPost")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Label(children="Nombre de fichiers uploadés : "),
        html.Label(id="nbfich")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Label(children="Nombre de réponses : "),
        html.Label(id="nbRep")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Label(children="Temps total sur le site : "),
        html.Label(id="tempsTotal")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Label(children="Délai de réponse moyen à un message : "),
        html.Label(id="delai")],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

##
# Insertion des données d'un étudiant sélectionné par l'utilisateur
@app.callback(
    Output("nbCo", "children"),
    Output("nbMessPost", "children"),
    Output("nbfich", "children"),
    Output("nbRep", "children"),
    Output("tempsTotal", "children"),
    Output("delai", "children"),
    Input("choix", "value"),
)
def affichage_donnees(option):
    data = dicoEleve["'"+option+"'"]
    return data['compteurConnexion'],data['compteurMsgPoste'],data['fichierUpload'],data['compteurMsgRep'],data['heureUtilisationSite'],data['delaiReponse']


if __name__ == '__main__':
    app.run_server(debug=True)