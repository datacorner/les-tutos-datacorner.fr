import yaml
import requests
import time
from datetime import datetime, timedelta, date
import pandas as pd

# INITIALISATION DE VARIABLES GLOBALES
sDateDebut = "2020-01-23"
sAujourdhui = date.today().strftime("%Y-%m-%d")
dDemarrageDate = datetime.fromisoformat(sDateDebut) 
cols = ['Date', 
        'FR Tot Cas Confirmés', 
        'FR Tot Décès', 
        'WW Tot Cas Confirmés', 
        'WW Tot Décès', 
        'Source',
        'FR Tot Guéris',
        'FR Tot Hospitalisés'
       ]

# FONCTIONS
def recupDataWithException2(_jsonout, _index1, _index2):
    try:
        data = _jsonout[_index1][_index2]
    except:
        data = 0
    return data

def AjouteSantePubliqueFrLigne(jsonout, df):
    df = df.append({
                    cols[0] : jsonout['date'] , 
                    cols[1] : recupDataWithException2(jsonout, 'donneesNationales', 'casConfirmes') , 
                    cols[2] : recupDataWithException2(jsonout, 'donneesNationales', 'deces'), 
                    cols[3] : recupDataWithException2(jsonout,'donneesMondiales', 'casConfirmes'),
                    cols[4] : recupDataWithException2(jsonout,'donneesMondiales', 'deces'),
                    cols[5] : 'sante-publique-france',
                    cols[6] : 0,
                    cols[7] : 0
                 } , 
                 ignore_index=True)
    return df

def ajouteLigneVide(df, madate):
    df = df.append({
                    cols[0] : madate , 
                    cols[1] : 0,
                    cols[2] : 0, 
                    cols[3] : 0,
                    cols[4] : 0,
                    cols[5] : 'no-data',
                    cols[6] : 0,
                    cols[7] : 0
                 } , 
                 ignore_index=True)
    return df

# RECUPERATION DONNEES SANTE PUBLIQUE FRANCE
def RecupereDonneesSantePubliqueFrance():
    print ('--> Démarrage du process')
    sDateParcours = sDateDebut
    i=1
    requesReturnCode=200
    yamls = pd.DataFrame()
    while (sDateParcours != sAujourdhui):
        myDate = dDemarrageDate + timedelta(days=i)
        sDateParcours = myDate.strftime("%Y-%m-%d")
        fichier = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/sante-publique-france/' + sDateParcours + '.yaml'
        #print ('--> sante-publique-france / ', sDateParcours)
        req = requests.get(fichier)
        requesReturnCode = req.status_code
        if (requesReturnCode==200):
            yamlout = yaml.load(req.text, Loader=yaml.FullLoader)
            yamls = AjouteSantePubliqueFrLigne(yamlout, yamls)
        else:
            print ("(*) Pas de données pour ", myDate.strftime("%Y-%m-%d"))
            # ajoute une ligne vide
            yamls = ajouteLigneVide(yamls, myDate.strftime("%Y-%m-%d"))
        i=i+1
    print ('--> Fin du process')
    return yamls

# RECUPERATION DONNEES SANTE PUBLIQUE FRANCE
def RecupereDonneesMinistereSante(yamls):
    i=1
    sDateParcours = sDateDebut
    print ('--> Démarrage du process')
    while (sDateParcours != sAujourdhui):
        myDate = dDemarrageDate + timedelta(days=i)
        sDateParcours = myDate.strftime("%Y-%m-%d")
        #print("Traintement date: ",  dateParcours)
        fichier = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/ministere-sante/' + sDateParcours + '.yaml'
        req = requests.get(fichier)
        requesReturnCode = req.status_code
        if (requesReturnCode==200):
            yamlout = yaml.load(req.text, Loader=yaml.FullLoader)
            if (yamls[cols[5]][i-1] == "no-data"):
                print ("(*) Modifie les données manquantes pour la date du ", myDate.strftime("%Y-%m-%d"))
                # Modifie toute la ligne
                yamls.loc[i-1, cols[1]] = recupDataWithException2(yamlout, 'donneesNationales', 'casConfirmes')
                yamls.loc[i-1, cols[2]]  = recupDataWithException2(yamlout, 'donneesNationales', 'deces')
                yamls.loc[i-1, cols[3]]  = recupDataWithException2(yamlout, 'donneesMondiales', 'casConfirmes')
                yamls.loc[i-1, cols[4]]  = recupDataWithException2(yamlout, 'donneesMondiales', 'deces')
                yamls.loc[i-1, cols[5]]  = "ministere-sante"
            # Ajoute les nouveaux champs
            yamls.loc[i-1, cols[6]] = recupDataWithException2(yamlout, 'donneesNationales', 'hospitalises')
            yamls.loc[i-1, cols[7]] = recupDataWithException2(yamlout, 'donneesNationales', 'gueris')
        i=i+1
    print ('--> Fin du process')
    return yamls

def Bouchetrous(yamls):
    # On reparcourre toutes les lignes déjà récupérées précédemment
    i=1
    for index, row in yamls.iterrows():
        if (yamls[cols[5]][i-1] == "no-data"):
            for j in [1, 2, 3, 4, 6, 7]:
                yamls.loc[i-1, cols[j]] = yamls[cols[j]][i-2] 
        i += 1
    return yamls

# Programme principal
print ("Récupération des données de Santé Publique France")
data = RecupereDonneesSantePubliqueFrance()
print ("Récupération des données du ministère de la santé")
data = RecupereDonneesMinistereSante(data)
print ("Comble les jours manquants")
data = Bouchetrous(data)

# quelques calculs
data['FR Nvx cas confirmés'] = 0
data['FR Nvx Décès'] = 0
data['FR Nvx Guéris'] = 0
data['FR Nvx Hospitalisés'] = 0

# Calcule les différence vs cumuls
for index, row in data.iterrows():
    if index > 0:
        data.loc[index, 'FR Nvx cas confirmés'] = data['FR Tot Cas Confirmés'][index] - data['FR Tot Cas Confirmés'][index-1] if (data['FR Tot Cas Confirmés'][index] - data['FR Tot Cas Confirmés'][index-1])>0 else 0
        data.loc[index, 'FR Nvx Décès'] = data['FR Tot Décès'][index] - data['FR Tot Décès'][index-1] if (data['FR Tot Décès'][index] - data['FR Tot Décès'][index-1])>0 else 0
        data.loc[index, 'FR Nvx Guéris'] = data['FR Tot Guéris'][index] - data['FR Tot Guéris'][index-1] if (data['FR Tot Guéris'][index] - data['FR Tot Guéris'][index-1] )>0 else 0
        data.loc[index, 'FR Nvx Hospitalisés'] = data['FR Tot Hospitalisés'][index] - data['FR Tot Hospitalisés'][index-1] if (data['FR Tot Hospitalisés'][index] - data['FR Tot Hospitalisés'][index-1] )>0 else 0

# Retire la dernière ligne (aujourd'hui) si pas de données récupérées
if (data.loc[len(data)-1,'Source'] == 'no-data'):
    data = data.drop([len(data)-1])
        
print ("Ecriture dans un fichier csv")
data.to_csv("./data/covid19_" + sAujourdhui + ".csv", index=False)
data.to_csv("./data/latest.csv", index=False)
