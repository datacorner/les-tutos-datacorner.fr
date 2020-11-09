from threading import Timer
import requests
import pandas as pd
from time import localtime, strftime

def update():
    getData()
    set_timer()
 
def set_timer():
    Timer(durationinsec, update).start()
 
def main():
    update()

# Cf infos sur https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/
def getData():
    global iteration
    #https://data.opendatasoft.com/explore/dataset/velib-disponibilite-en-temps-reel%40parisdata/api/
    nbrows = 1500
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel%40parisdata&rows=" + str(nbrows) + "&facet=overflowactivation&facet=creditcard&facet=kioskstate&facet=station_state"
    mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    resp = requests.get(url)
    if resp.status_code != 200:
        print(mytime, " - ", iteration, " - Erreur dans la récupération des données")
    else:
        data = resp.json()
        dff = pd.DataFrame(columns =['Timer', 'ID', 'Station', 'Code Station', 'Type de stations', 'Etat de la station',
                                     'Nb bornes disponibles', 'Nombres de bornes en station', 'Nombre vélo en PARK+',
                                     'Nb vélo mécanique', 'Nb vélo électrique',
                                     'geo'])
        for rec in data['records']:
            dff.loc[len(dff)] = [mytime, 
                                 rec['recordid'],
                                 rec['fields']['station_name'],
                                 rec['fields']['station_code'],
                                 rec['fields']['station_type'],
                                 rec['fields']['station_state'],
                                 rec['fields']['nbfreeedock'],
                                 rec['fields']['nbedock'],
                                 rec['fields']['nbbikeoverflow'],
                                 rec['fields']['nbbike'],
                                 rec['fields']['nbebike'],
                                 rec['fields']['geo']]
        if int(data['nhits']) > 0:
            with open("vélib_batch_parheure.csv", 'a') as f:
                dff.to_csv(f, header=True, index=False)
            print(mytime, " - ", iteration, " - Fin de la récupération, Nb de lignes récupérées: ", data['nhits'])
        else:
            print(mytime, " - ", iteration, " - Pas de données à récupérer.")
    iteration = iteration + 1
    
#----------------------------------------
    
durationinsec = 1*60*60
iteration = 1    
main()
