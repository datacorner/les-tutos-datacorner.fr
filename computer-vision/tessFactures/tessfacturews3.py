from flask import Flask, request, Response
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import json
import jsonpickle
import numpy as np
import cv2
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

app = Flask(__name__)

# Remove empty lines from a given string
def RemoveEmptyLines(entree):
    tab = entree.strip()
    tableausansvide = [ x for x in tab.splitlines() if x!='' ]
    res = ''
    for i in range(0, len(tableausansvide)):
        res = res + tableausansvide[i] + '\n'
    return res

# Get the string bettween two tag strings (and remove empty lines in between)
def getTextBetween(mainString, startWord, endWord):
    start = mainString.find(startWord) + len(startWord)
    end = mainString.find(endWord)
    return RemoveEmptyLines(mainString[start:end])

# get the PO details in the specific invoice
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

@app.route('/check')
def index():
    output = {}
    output['status'] = "Service running"
    # Preprare respsonse, encode JSON to return
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/facture', methods=['POST'])
def invoice():
    r = request
    # convert string of image data to uint8
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    output = {}
    pytesseract.pytesseract.tesseract_cmd = r'tesseract-4.0.0.exe'
    resultat = pytesseract.image_to_string(image)
    print (resultat)
    output["Adresse"] = getTextBetween(resultat, 'www.blueprism.com/fr', 'Référence').strip()
    output["Reference"] = getTextBetween(resultat, 'Référence: ', 'Date: ').strip()
    output["DateFacture"] = getTextBetween(resultat, 'Date: ', 'Client: ').strip()
    output["CodeClient"] = getTextBetween(resultat, 'Client: ', 'Intitulé: ').strip()
    
    # Récupération des lignes de PO
    pos = getTextBetween(resultat, 'Prix total HT', 'Total HT ')
    tabPOs = pos.splitlines()
    output["NbPo"] = len(tabPOs)
    pos = []
    for i in range(0, len(tabPOs)):
        pos.append(getPosElement(tabPOs[i]))
    output['po'] = pos
    output["totalht"] = getTextBetween(resultat, 'Total HT ', 'TVA (20%) ').strip()
    output["tva"] = getTextBetween(resultat, 'TVA (20%) ', 'Total TTC (en euros) ').strip()
    output["total"] = getTextBetween(resultat, 'Total TTC (en euros) ', '\nEn votre aimable reglement,').strip()
    
    # Preprare respsonse, encode JSON to return
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/image', methods=['POST'])
def generic():
    r = request
    # convert string of image data to uint8
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    output = {}
    pytesseract.pytesseract.tesseract_cmd = r'tesseract-4.0.0.exe'
    resultat = pytesseract.image_to_string(image)
    print (resultat)
    output['output'] = resultat
    
    # Preprare respsonse, encode JSON to return
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/pdf', methods=['POST'])
def pdf():
    r = request.data
    output = {}
    pytesseract.pytesseract.tesseract_cmd = r'tesseract-4.0.0.exe'
    images = convert_from_bytes(r)
    print ("Nombre de pages: " + str(len(images)))
    for i in range(len(images)):
        resultat = pytesseract.image_to_string(images[i]) + "\n"
        if (len(images) > 1):
            resultat = resultat + "----TESSFACTURE----"
    
    print (resultat)
    output['output'] = resultat
    
    # Preprare respsonse, encode JSON to return
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)