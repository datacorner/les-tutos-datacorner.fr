from flask import Flask
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import json

app = Flask(__name__)

def RemoveEmptyLines(entree):
    tab = entree.strip()
    tableausansvide = [ x for x in tab.splitlines() if x!='' ]
    res = ''
    for i in range(0, len(tableausansvide)):
        res = res + tableausansvide[i] + '\n'
    return res

def getTextBetween(mainString, startWord, endWord):
    start = mainString.find(startWord) + len(startWord)
    end = mainString.find(endWord)
    return RemoveEmptyLines(mainString[start:end])

def getPosElement(po):
    element = {}
    element['quantite'] = po[0:po.find (' ')].strip()
    po = po[po.find (' '):len(po)]
    element['prixtotht'] = po[po.rfind (' '):len(po)].strip()
    po = po[0:po.rfind (' ')]
    element['prixunitht'] = po[po.rfind (' '):len(po)].strip()
    po = po[0:po.rfind (' ')]
    element['decription'] = po.strip()
    return element

@app.route('/')
def index():
    return "Lecture de fichier de factures"

@app.route('/factures/<num>')
def order(num):
    fichier = r'Facture_' + str(num) + r'.jpg'
    image = Image.open(fichier)
    output = {}    
    resultat = pytesseract.image_to_string(image)
    output["Adresse"] = getTextBetween(resultat, 'www.blueprism.com/fr', 'Référence').strip()
    output["Reference"] = getTextBetween(resultat, 'Référence: ', 'Date: ').strip()
    output["DateFacture"] = getTextBetween(resultat, 'Date: ', 'Client: ').strip()
    output["CodeClient"] = getTextBetween(resultat, 'Client: ', 'Intitulé: ').strip()
    
    # Récupération des lignes de PO
    pos = getTextBetween(resultat, 'Prix total HT', 'Total HT ')
    tabPOs = pos.splitlines()
    print ('Nombre de PO: ' + str(len(tabPOs)))
    output["NbPo"] = len(tabPOs)
    pos = []
    for i in range(0, len(tabPOs)):
        pos.append(getPosElement(tabPOs[i]))
    output['po'] = pos
    output["totalht"] = getTextBetween(resultat, 'Total HT ', 'TVA (20%) ').strip()
    output["tva"] = getTextBetween(resultat, 'TVA (20%) ', 'Total TTC (en euros) ').strip()
    output["total"] = getTextBetween(resultat, 'Total TTC (en euros) ', 'En votre aimable réglement,').strip()
    
    return output

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)