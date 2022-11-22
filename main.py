import getDataIndicateur as gDI
import json
import codecs
jsonopen=open("traceforum.json", "r")
f = json.load(jsonopen)

listeUser= gDI.listeUstilisateur(f["transition"])
dicoUser=gDI.creationDicoUser(listeUser)
dicoUser=gDI.calculNbConnexionNbMsgPoste(dicoUser,f["transition"])
dicoEleve,dicoEnseignant, dicoInactif = gDI.separationEleveEnseignant(dicoUser,listeUser,f["transition"])

print(dicoEleve)
jsonopen.close()