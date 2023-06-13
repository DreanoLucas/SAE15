import csv 
from os import mkdir

def creation_dossier(): #Crée les répértoires s'ils n'existent pas
    try:
        mkdir('./html')
    except:
        pass
    try:
        mkdir('./csv')
    except:
        pass
    try:
        mkdir('./css')
    except:
        pass


def LigneCount(): 
    ligne=list()
    Nombre=dict()
    file=open("sanitaires-reseau-ratp.csv","r") #ouverture du fichier csv
    csvreader=csv.reader(file,delimiter=";") #lecture du fichier csv avec comme separateur de valeur ";"
    header=next(csvreader)  
    for row in csvreader: #boucle qui compte le nombre d'iteration d'une ligne dans le fichier csv dans un dictionnaire relié au nom de la ligne
        ligne.append(row[0]) #liste des lignes
        if row[0] in Nombre.keys():
            Nombre[row[0]] += 1
        else:
            Nombre[row[0]]=1
    return ligne,Nombre    


def creaCSVcompte(Nombre,Gratuit:dict,PourcentageGratuit:dict):
    file=open("./csv/ligne.csv","w")
    fieldnames=["Lignes","Nombre de sanitaires disponibles","Nombre de sanitaires gratuit","Pourcentage de sanitaire gratuit"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for k, v in Nombre.items(): #utilisation des valeurs du dictionnaire
        valeurGratuit =  Gratuit[k] #On cree des variable intermediaires afin de contenir les valeurs du dictionnaire 
        valeurPourcentageGratuit = PourcentageGratuit[k]
        writer.writerow({"Lignes":k ,"Nombre de sanitaires disponibles":v,"Nombre de sanitaires gratuit":valeurGratuit,"Pourcentage de sanitaire gratuit":valeurPourcentageGratuit}) 
    file.close()    

def AccesGratuit(): #Nombre de sanitaire accessible gratuitement pour chaque ligne  
    ligne=dict()
    file=open("sanitaires-reseau-ratp.csv","r")
    csvreader=csv.reader(file,delimiter=";")
    header=next(csvreader)
    for row in csvreader:
        if row[3]=="gratuit":
            if row[0] in ligne.keys():
                ligne[row[0]] += 1
            else:
                ligne[row[0]]=1
        else:
            if row[0] in ligne.keys():
                pass
            else:
                ligne[row[0]]=0
    return ligne 

def pourcentage(gratuit,ligne):
    dico=dict()
    for k in gratuit.keys():
        pourcentage=(int(gratuit[k]/ligne[k]*100)) #calcul du pourcentage de sanitaire gratuit par ligne.
        dico[k] = pourcentage #dictionnaire associant ligne et pourcentage
    return(dico)

def HTML(nom): #creation du fichier HTML principal
    htmlout=open("./html/ligne.html","w",encoding='utf-8') #Creation du fichier en .html dans le dossier html
    htmlout.write("<!DOCTYPE html>")  #Entêtes HTML
    htmlout.write("""<html> \n <head><meta charset='utf-8'> <link rel="stylesheet" href="../css/style.css"> <title>index</title> <link rel="icon" href="https://upload.wikimedia.org/wikipedia/fr/thumb/0/01/RATP.svg/langfr-800px-RATP.svg.png" > </head> \n <body> \n""")
    htmlout.write("<table>\n <thead> <tr>") #declaration du debut du tableau 
    file=open('./csv/'+str(nom)+".csv","r")
    csvlistreader = csv.reader(file)
    for fisrtline in csvlistreader: 
        for keys in fisrtline:
            htmlout.write("<th>{}</th>".format(keys)) 
        break
    htmlout.write("</tr></thead>")
    htmlout.write("<tbody>")
    for row in csvlistreader:
        try:
            html= "<tr>"
            html += "<td><a href=ligne{}.html>{}</a></td>".format(row[0],row[0])
            html += "<td>{}</td>".format(row[1])
            html += "<td>{}</td>".format(row[2])
            html += "<td>{}%</td>".format(row[3])
            html += "</tr>"
            htmlout.write(html)
        except:
            pass
    fin_html = "</table>"
    fin_html += "<a href=../index.html>Retour à la page de présentation</a>"
    htmlout.write(fin_html)

def CSVparligne(): #Fichier csv pour chaque ligne où on retrouve les informations sur les sanitaires de chaque station de la ligne
    file=open("sanitaires-reseau-ratp.csv","r")
    csvreader=csv.DictReader(file,delimiter=";")
    header=next(csvreader)
    openFiles=dict()
    for row in csvreader:
        ligne = row['ligne']
        if ligne in openFiles.keys():
            openFiles[ligne].writerow(row)
        else:
            outfile=open("./csv/ligne"+ligne+".csv","w")
            writer = csv.DictWriter(outfile, fieldnames=header)
            writer.writeheader()
            writer.writerow(row)
            openFiles[ligne] = writer                          

def HTMLligne(): #creons les HTML à partir des CSV généré
    file=open('sanitaires-reseau-ratp.csv','r')
    csvreader=csv.DictReader(file,delimiter=";")
    header=next(csvreader)
    from os import listdir
    listpath= listdir("./csv") #Creation d'une liste de tout les fichiers dans le dossier CSV
    listlignecsv = []
    for elem in listpath: 
        if ((elem[len(elem)-4:] == ".csv") and (elem[:5] == "ligne") and (len(elem) > 9)): #On filtre les fichiers csv pour garder ceux généré
            listlignecsv.append(elem)
    for ligne in listlignecsv:
        htmlout=open("./html/"+ligne.replace('csv','html'),"w") #Enleve le .csv et le remlace par .html et cree le fichier correspondant
        htmlout.write("<!DOCTYPE html>")
        htmlout.write(""" <html> \n <head><meta charset='utf-8'> <link rel="stylesheet" href="../css/style.css"> <title>Sanitaire sur la ligne</title> <link rel="icon" href="https://upload.wikimedia.org/wikipedia/fr/thumb/0/01/RATP.svg/langfr-800px-RATP.svg.png"> </head> \n <body> \n""")
        htmlout.write("<table>\n <thead> <tr>")
        csvfile=open("./csv/"+ligne,'r') #ouverture du fichier csv portant le nom de la ligne
        csvlistreader=csv.reader(csvfile)
        for fisrtline in csvlistreader: #ecrire pour chaque fichier csv un fichier html avec tableau
            for keys in fisrtline:
                htmlout.write(" <th>{}</th>".format(keys))
            break
        htmlout.write("</tr></thead>")
        htmlout.write("<tbody>")
        for row in csvlistreader:
            try:
                code_html= "<tr>"
                for i in range(len(row)):
                    if row[i]=="":
                        row[i]="non"
                    code_html+= "<td>{}</td>".format(row[i])
                code_html += "</tr>"
                htmlout.write(code_html)
            except:
                print('erreur inattendue')
                pass
        fin_du_html = "</table>"
        fin_du_html +="<a href='./ligne.html'>Retour</a>"
        htmlout.write(fin_du_html)
            

       
def fixed(): #Permet de retirer les lignes vides dans les csv
    from os import listdir

    csvlist = listdir("./csv/")
    for elem in csvlist: 
        if elem[len(elem)-4:] == ".csv": #ouvre chaque csv 
            f = open('./csv/'+elem, "r") 
            text = f.read().replace("\n\n", "\n") #enleve les sauts de ligne
            f = open('./csv/'+elem, "w")
            f.write(text) #réécris les fichiers csv

def generation_css():
    file=open("./css/style.css","w")
    file.write("""table {
   margin: 20px auto;
   border-collapse: collapse;
   font-size: 18px;
   font-family: sans-serif;
   min-width: 800px;
   box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
 }
 
 table {
   border-collapse: collapse;
 }
 
 td, th {
   border: 1px solid black;
   padding: 10px;
   text-align: center;
 }
 
 td:hover {
   background-color: #f5f5f5;
   cursor: pointer;
   transform: scale(1.1);
   transition: all 0.3s ease-in-out;
 }
 
 th {
   background-color: #4CAF50;
   color: #fff;
   font-weight: bold;
 }
 
 tr:hover {
   background-color: #f5f5f5;
 }
 
 a {
   display: block;
   margin: 20px auto;
   text-align: center;
   text-decoration: none;
   font-size: 20px;
   color: #4CAF50;
   font-weight: bold;
 }
 
 a:hover {
   text-decoration: underline;
   color: blue;
 }""")

creation_dossier()
ListeLigne,NombreDeSanitaireParLigne = LigneCount()
NombreDeSanitaireGratuitParLigne = AccesGratuit()
PourcentageDeSanitaireGratuit = pourcentage(NombreDeSanitaireGratuitParLigne,NombreDeSanitaireParLigne)
creaCSVcompte(NombreDeSanitaireParLigne,NombreDeSanitaireGratuitParLigne,PourcentageDeSanitaireGratuit)
fixed()
CSVparligne()
fixed()
print('fichiers CSV généré')
HTML("ligne")
print('fichiers HTML généré')
HTMLligne()
generation_css()
print("Tout les fichiers ont été généré correctement")


