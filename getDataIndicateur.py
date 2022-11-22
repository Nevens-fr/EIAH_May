from scipy import *
from datetime import datetime
import calendar
import math
import numpy as np 
#Permet de renvoyer le nombre de connexion ainsi que le nombre de message posté
def calculNbConnexionNbMsgPoste(dicoUser,data):
    for item in data :
        if  item["Titre"] == "'Connexion'":
            dicoUser[item["Utilisateur"]]['compteurConnexion']+=1
        elif item["Titre"] == "'Poster un nouveau message'":
            dicoUser[item["Utilisateur"]]['compteurMsgPoste']+=1
        elif item["Titre"] == "'Upload un ficher avec le message'":
            dicoUser[item["Utilisateur"]]['fichierUpload']+=1
        elif item["Titre"] == "'Répondre à un message'":
            dicoUser[item["Utilisateur"]]['compteurMsgRep']+=1
            
    return dicoUser

#Permet de récupérer la liste des utilisateurs 
def listeUstilisateur(data):
    listeUser=[]
    for item in data : 
        listeUser.append(item["Utilisateur"])
        listeUser[:]=list(set(listeUser))
    return listeUser

#Permet d'associer les utilisateurs aux différents indicateurs
def creationDicoUser(listeuser):
    dicoUser={}
    for item in listeuser :
        dicoUser[item]={'compteurConnexion' : 0,'compteurMsgPoste' : 0,'fichierUpload':0, 'compteurMsgRep':0,'heureUtilisationSite': 0,'delaiReponse':0,'nbMessageNonVu':0}
    return dicoUser

#Permet de renvoyer le nombre de connexion ainsi que le nombre de message posté de référence
def moyenneFichierUploadAllPerson(listeUser,data):
    tauxCompteurConnexion=0
    compteurMsgPoste = 0
    compteurFichierUpload=0
    for item in data :
        if item["Titre"]== "'Connexion'":
            tauxCompteurConnexion+=1
        elif item["Titre"] == "'Poster un nouveau message'":
            compteurMsgPoste+=1
        elif item["Titre"] == "'Upload un ficher avec le message'":
            compteurFichierUpload+=1
    return (compteurFichierUpload / len(listeUser))

#Permet de récupérer un dictionnaire d'élève et un dictionnaire d'enseignant et un dictionnaire de personne inactif
def separationEleveEnseignant(dicoUser,listeUser,data):
    dicoEleve={}
    dicoEnseignant={}
    dicoCompteInactif={}
    valRefFichierUpload = moyenneFichierUploadAllPerson(listeUser,data)
    #On part du principe que les élèves ont posté beaucoup de message et intéragit plus sur le site par rapport au enseignant
    for item in listeUser:
        #On part sur inférieur a 10 car soit un prof soit inactif
        if(dicoUser[item]["compteurMsgPoste"]<10):
            #Si il y a des uploads c'est que c'est un élève
            if(dicoUser[item]["fichierUpload"]>valRefFichierUpload):
                dicoEleve[item]=dicoUser[item]
            #Si il n'y a pas de connexions ou de messages postés c'est que la personne est totalement inactif
            elif(dicoUser[item]["compteurConnexion"]==0 or dicoUser[item]["compteurMsgPoste"]==0 or item=="'admin'"):
                dicoCompteInactif[item]=dicoUser[item]
            #Si une personne après l'écrémage a moins de 5 messages on le compte comme un élève car les professeurs ont tendance à répondre aux élèves
            elif (dicoUser[item]["compteurMsgRep"]<=5):
                dicoEleve[item]=dicoUser[item]
            else :
                dicoEnseignant[item]=dicoUser[item]
        else :
            dicoEleve[item]=dicoUser[item]
    return dicoEleve,dicoEnseignant,dicoCompteInactif


#Permet de récupérer la moyenne  nombre d'heure sur toutes les journées
def heureUtilisationSite(user,data):
    tabidmsgenvoyer=[]
    for item in data :
        if item["Titre"] == "'Connexion'" and user==item["Utilisateur"]:
            tabidmsgenvoyer.append(item["Date"])
            tabidmsgenvoyer[:]=list(set(tabidmsgenvoyer))

    debheure = [""]*(len(tabidmsgenvoyer))
    tabdate=[""]*(len(tabidmsgenvoyer))
    for i in range(len(tabidmsgenvoyer)) :
        for item in data :
            if user==item["Utilisateur"] and item["Date"]==tabidmsgenvoyer[i]:
                if item["Titre"] == "'Connexion'" and debheure[i]=="":
                    debheure[i]=item["Heure"].replace("'", '')
                else:
                    tabdate[i] = item["Heure"].replace("'", '')
    tabheure = []
    for i in range(len(tabidmsgenvoyer)):
        if debheure[i]==''or tabdate[i]=='' :
            tabheure.append(0)
        else:
            ptdebheure = datetime.strptime(debheure[i],'%H:%M:%S')
            total_seconds_debheure = ptdebheure.second + ptdebheure.minute*60 + ptdebheure.hour*3600
            pttabdate = datetime.strptime(tabdate[i],'%H:%M:%S')
            total_seconds_tabdate = pttabdate.second + pttabdate.minute*60 + pttabdate.hour*3600
            tabheure.append(total_seconds_tabdate-total_seconds_debheure)
    return np.sum(tabheure)/len(tabheure)
    
#Permet de calculer le Delai entre l'envoie du premier message et l'affichage de la réponse au message
def calulDelaiReponseMessage(user,data):
    posternewmessagedate=[]
    posteridnewmessage=[]
    repondrenewmessage=[]
    compteurmessagenonlu=0
    for item in data:
        if item["Titre"]=="'Poster un nouveau message'" and user==item["Utilisateur"]:
            posternewmessagedate.append(item["Date"].replace("'", ''))
            posteridnewmessage.append(item["Attribut"].split(',')[1].split('=')[1])
    repondrenewmessage=[""]*(len(posteridnewmessage))
    for i in range(len(posteridnewmessage)) :
        for ligne in data:
            if (user==ligne["Utilisateur"]) and (ligne["Titre"]=="'Afficher le contenu d''un message'" or ligne["Titre"]=="'Répondre à un message'") :
                if(ligne["Titre"]=="'Répondre à un message'" and ligne["Attribut"].split(',')[2].split('=')[1]== posteridnewmessage[i]):
                    repondrenewmessage[i]=(ligne["Date"].replace("'", ''))
                elif(ligne["Attribut"].split(',')[1].split('=')[1] == posteridnewmessage[i]):
                    repondrenewmessage[i]=(ligne["Date"].replace("'", ''))

    delaiReponse=[]

    for i in range(len(posteridnewmessage)) : 
        if(repondrenewmessage[i]=='' or posternewmessagedate[i]==''):
            compteurmessagenonlu+=1
        else:
            ptpostmsg= datetime.strptime(posternewmessagedate[i],"%Y-%m-%d")
            total_seconds_postmsg = calendar.timegm(ptpostmsg.timetuple())
            ptnewmessage = datetime.strptime(repondrenewmessage[i],"%Y-%m-%d")
            total_seconds_newmessage= calendar.timegm(ptnewmessage.timetuple())
            delaiReponse.append(total_seconds_newmessage-total_seconds_postmsg)
            
    if math.isnan(((np.sum(delaiReponse)/(len(posteridnewmessage)-compteurmessagenonlu))/60)) == False:
        return ((np.sum(delaiReponse)/(len(posteridnewmessage)-compteurmessagenonlu))/60)/60,compteurmessagenonlu
    else:
        return 0, compteurmessagenonlu



##
# Calculer les moyennes globales
def calculerMoyennes(data):
    mean = [0,0,0,0]
    nb = 0

    for personne,donnees in data.items():
        for key,val in donnees.items():
            if key == "compteurConnexion":
                mean[0] = val + mean[0]
            elif key == "compteurMsgPoste":
                mean[1] += val
            elif key == "heureUtilisationSite":
                mean[2] += val
            elif key == "delaiReponse":
                mean[3] += val
        nb +=1

    i = 0

    while i < len(mean):
        if mean[i] != 0:
            mean[i] = mean[i] / nb
        i+=1
    return mean

#Retourne les données d'un dictionnaire sous la forme de liste
def getDataList(data):
    return [data["compteurConnexion"],data["compteurMsgPoste"],data["heureUtilisationSite"],data["delaiReponse"]]