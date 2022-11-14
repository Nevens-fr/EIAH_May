import json
import codecs

#Parser de données dans un fichier sql
class parserSQL():

    ##
    # Initialisation de l'instance de classe
    # filename : nom du fichier à parser
    def __init__(self, filename):
        print("Création du parser de SQL")
        self.filename = filename

    ##
    # Le fichier sql en entrée est parsé et un fichier cible est écrit
    # cible : nom du fichier cible
    def parser(self, cible):
        print("Parsing en cours")

        self.cible = cible

        f = codecs.open(self.filename, "r",  "utf-8")

        tables = {}
        ind = 0
        courant = ind
        headers = []
        data = []
        erreur = False

        try:
            for line in f:

                #on trouve un nouvel insert
                if ("INSERT INTO" in line) or ("insert into" in line):
                    #récupération du nom de la table
                    tablename = line.split(" ", 1)[1].split(" ", 1)[1].split("(", 1)[0]
                    tablename = tablename.replace('`', '')
                    tablename = tablename.replace(' ', '')

                    #récupération des noms des colonnes
                    raws = line.split(" ", 1)[1].split(" ", 1)[1].split("(", 1)[1].split(")", 1)[0]
                    raws = raws.replace('`', '')
                    raws = raws.replace(' ', '')

                    #création d'une nouvelle entrée si on ne possède pas déjà cette table
                    if tablename not in tables:
                        headers.append(raws)
                        data.append([])
                        tables[tablename] = ind
                        ind += 1
                        courant = ind - 1
                    #on récupère l'info pour stocker les données au bon endroit
                    else:
                        courant = tables[tablename]
                #on récupère les données insérées
                elif line[0] == "(":
                    lineR = line.split("(", 1)[1]
                    lineR = lineR.replace("),\n", "")
                    data[courant].append(lineR) 
        except Exception as e:
            print("Erreur lors du parsing : " + str(e))
            erreur = True
        f.close()
    
        if not erreur:
            self.ecriture(tables, headers, data)

    ##
    # Ecriture des données dans le fichier json cible
    # tables : noms des tables
    # headers : nom des colonnes
    # data : données par table
    def ecriture(self, tables, headers, data):
        f = codecs.open(self.cible, "w",  "utf-8")

        result = {}

        #organisation des données par table
        for key, value in tables.items():
            #tableau json/liste qui contiendra les données de la table
            result[key] = []

            #récupération de toutes les clefs pour une table
            colonnes = headers[value].split(",")

            #parcours de toutes les données d'une table
            for a in data[value]:
                d = a.split(", ")
                ind = 0

                #création de l'object json/ dictionnaire, correspondant à une entrée de la table
                result[key].append({})

                #insertion des données de la table dans les clefs correspondantes
                while ind < len(d):
                    result[key][-1][colonnes[ind]] = d[ind]
                    ind +=1

        f.write(json.dumps(result, indent=4,ensure_ascii=False,sort_keys = True))
        f.close()

f = json.load(open("traceforum.json", "r"))

print(f["activite"])