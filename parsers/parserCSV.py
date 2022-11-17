import json
import codecs

#Parser de données dans un fichier CSV
class parserCSV():

    ##
    # Initialisation de l'instance de classe
    # filename : nom du fichier à parser
    def __init__(self, filename):
        print("Création du parser de CSV")
        self.filename = filename

    ##
    # Le fichier csv en entrée est parsé et un fichier cible est écrit
    # cible : nom du fichier cible
    def parser(self, cible):
        print("Parsing en cours")

        self.cible = cible

        f = codecs.open(self.filename, "r",  "utf-8")

        header = f.readline().replace("\n","").replace("\r","").split(";")

        lines = f.readlines()

        f.close()

        res = []

        #Création d'un tableau contenant les données json
        for line in lines:
            obj = {}
            data = line.replace("\n", "").replace("\r","").split(";")
            i = 0

            #ajout des données dans les objets
            while i < len(data):
                obj[header[i]] = data[i]
                i+=1
            
            res.append(obj)

        #sauvegarde du nouveau fichier
        f = codecs.open(self.cible, "w",  "utf-8")
        f.write(json.dumps(res, indent=4,ensure_ascii=False,sort_keys = True))
        f.close()