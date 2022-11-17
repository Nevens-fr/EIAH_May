import parsers.parserSQL as parserSQL
import parsers.parserCSV as parserCSV
import sys

#Parser générique permettant de transformer en json n'importe quel fichier
class parserGenerique:

    ##
    # Initialisation de l'instance de classe
    # filename : nom du fichier à parser
    def __init__(self, filename):
        print("Création du parser générique")
        self.filename = filename
        self.extension = filename.rsplit('.', 1)[1]
        self.cible = self.filename.rsplit('.', 1)[0] + ".json"


    ##
    # Le fichier en entrée est parsé selon son type, on retourne le nom du fichier cible
    def parser(self):
        if self.extension == "json":
            print("Fichier déjà au bon format")
            return self.cible
        elif self.extension == "sql":
            parserSQL.parserSQL(self.filename).parser(self.cible)
            return self.cible
        elif self.extension == "csv":
            parserCSV.parserCSV(self.filename).parser(self.cible)
            return self.cible

#Lecture du fichier à parser via la ligne de commande
try:
    print('\nFichier à parser : ' + str(sys.argv[1]) + "\n")
    a = parserGenerique(sys.argv[1])
    print("\nLe fichier parsé se nomme : " + a.parser() + "\n")
except:
    print("\nUtilisation : python parserGenerique fichierAParser\n")