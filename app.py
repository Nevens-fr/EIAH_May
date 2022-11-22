# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

import getDataIndicateur as gDI
import json

app = Dash(__name__)

#lecture et classification des données
jsonopen=open("traceforum.json", "r")
f = json.load(jsonopen)


listeUser= gDI.listeUstilisateur(f["transition"])
dicoUser=gDI.creationDicoUser(listeUser)
dicoUser=gDI.calculNbConnexionNbMsgPoste(dicoUser,f["transition"])
dicoEleve,dicoEnseignant, dicoInactif = gDI.separationEleveEnseignant(dicoUser,listeUser,f["transition"])
for cle,valeur in dicoEleve.items():
    valeur["heureUtilisationSite"]=(gDI.heureUtilisationSite(cle,f["transition"])/60)
    valeur["delaiReponse"],valeur["nbMessageNonVu"]=gDI.calulDelaiReponseMessage(cle,f["transition"])

jsonopen.close()

moyennes = gDI.calculerMoyennes(dicoEleve)

#création des figures et ensembles de données
eleves = []

for cle,valeur in dicoEleve.items():
    eleves.append(cle.replace("'",""))

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.DataFrame({
    "Indicateurs":["Nombre de connexions", "Nombre de messages postés", "Temps total sur le site (minutes)", "Délai (heures)","Nombre de connexions", "Nombre de messages postés", "Temps total sur le site (minutes)", "Délai (heures)"],
    "Valeurs" : moyennes+gDI.getDataList(dicoEleve["'"+eleves[0]+"'"]),
    "Type": ["Moyenne","Moyenne","Moyenne","Moyenne","Etudiant","Etudiant","Etudiant","Etudiant"]
})

fig = px.bar(df, x="Indicateurs", y="Valeurs", color="Type", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#création de la mise en page
app.layout = html.Div(style={'backgroundColor': colors['background']},children=[

    html.Div(children="Choissez un élève pour lequel vous souhaitez visualiser des indicateurs"),

    dcc.Dropdown(
        eleves,
        eleves[0],
        id="choix"
    ),

    html.Br(),

    dcc.Graph(
        id='graph',
        figure=fig
    )
])

##
# Insertion des données d'un étudiant sélectionné par l'utilisateur
@app.callback(
    Output("graph", "figure"),
    Input("choix", "value"),
)
def affichage_donnees(option):
    df = pd.DataFrame({
    "Indicateurs":["Nombre de connexions", "Nombre de messages postés", "Temps total sur le site (minutes)", "Délai (heures)","Nombre de connexions", "Nombre de messages postés", "Temps total sur le site (minutes)", "Délai (heures)"],
    "Valeurs" : moyennes+gDI.getDataList(dicoEleve["'"+option+"'"]),
    "Type": ["Moyenne","Moyenne","Moyenne","Moyenne","Etudiant","Etudiant","Etudiant","Etudiant"]
    })

    fig = px.bar(df, x="Indicateurs", y="Valeurs", color="Type", barmode="group")

    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)