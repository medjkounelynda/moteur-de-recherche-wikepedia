import xml.etree.ElementTree as ET
import re
import time
import math
from nltk.corpus import stopwords
from matricecreuse import MatriceCreuse as mcreuz


pref = '{http://www.mediawiki.org/xml/export-0.10/}'
fichierMotEnlever='motExit.xml'
fichierCorpus='wiki_musique.xml'
racine = '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="fr">'


class Dico:
    """docstring for Dictionnaire."""

    def __init__(self, name_file,fichierMotAEnlever):
        self.name_file = name_file
        self.fichierMotAEnlever=fichierMotAEnlever

        self.dicoliste={}
        self.listeTitre=[]
        self.DicoTitre={}

    def avoirDicoMot(self,txt,dic,stop_wordsFrench,stop_wordsEnglish,numberPage):
            word_tokens=txt.split()
            long= len(word_tokens)
            if long>0 :
                frequence = 1
            else : return dic
            aux={}
            for mot in word_tokens:
                if mot not in stop_wordsFrench and mot not in stop_wordsEnglish:
                    if mot not in aux.keys():
                        aux[mot]=(numberPage,frequence)
                    else:
                        nbp,freq = aux[mot]
                        freq+=frequence
                        aux[mot]=(nbp,1+math.log10(freq))
            sommeNormal=0
            for cle,val in aux.items():
                sommeNormal=sommeNormal+(val[1]*val[1])
            sommeNormal=math.sqrt(sommeNormal)
            for cle,val in aux.items():
                aux[cle]=(val[0],val[1]/sommeNormal)

            """aux1={cle:val for cle,val in aux.items() if val[1]>0.001}"""
            for cle,val in aux.items():
                if cle in dic.keys():
                    listePage=dic[cle]
                    listePage.append(val)
                    dic[cle]=(listePage)
                else:
                    dic[cle]=([val])
            return dic

    def formatageTexte(self,txt):
        txt = txt.lower()
        txt = re.sub('\s+','  ',txt)
        txt = re.sub('<[^>]+>|\[\[?|\]\]?|\{\{|\}\}|\||:|=+|\W|([0-9]{1,3})', ' ',txt) # les balises
        txt = re.sub(r"'", " ",txt)
        return txt



    def nettoyage_texte(self):
            dic={}

            stop_wordsFrench = set(stopwords.words('french'))
            for line in open(self.fichierMotAEnlever,'r'):
                for mot in line.split():
                    stop_wordsFrench.add(mot)
            numberPage=0
            stop_wordsEnglish = set(stopwords.words('english'))
            for event, elem in ET.iterparse(self.name_file):
                if elem.tag == pref+'page':
                    txt = elem.find(pref+'revision/'+pref+'text').text
                    txt=self.formatageTexte(txt)
                    dic=self.avoirDicoMot(txt, dic ,stop_wordsFrench , stop_wordsEnglish, numberPage)
                    title=elem.find(pref+'title').text
                    self.listeTitre.append(title)
                    self.DicoTitre[title]=numberPage

                    numberPage+=1
                    print(numberPage)


            for cle,val in dic.items():
                self.dicoliste[cle]=(val,math.log10(numberPage/len(val)))

            print(self.DicoTitre)


    def saveDic(self,fichierSortie):


        with open(fichierSortie,"w") as fS:
            for cle,val in self.dicoliste.items():
                fS.write(cle)
                listePage=val
                for page in listePage:
                    fS.write(";"+str(page))
                fS.write("\n")

    def genererCLI(self):
        self.fichierL='fichierL.txt'
        self.fichierC='fichierC.txt'
        self.fichierI='fichierI.txt'

        with open(self.fichierL,'w') as fL, open(self.fichierC,'w') as fC, open (self.fichierI,'w') as fI:
            fL.write(str(0)+"\n")
            k=0
            for event, elem in ET.iterparse(self.name_file):
                if elem.tag == pref+'page':
                    lienExternePage=[]
                    texte = elem.find(pref+'revision/'+pref+'text').text
                    liens=re.findall(r'\[\[(.*?)\]\]',texte)
                    for lien in liens:
                        if lien in self.listeTitre and lien not in lienExternePage:
                            lienExternePage.append(lien)


                    nombreLiens=0
                    for i in range(len(self.listeTitre)):
                        if self.listeTitre[i] in lienExternePage:
                            fI.write(str(self.DicoTitre[self.listeTitre[i]])+"\n")
                            print(self.DicoTitre[self.listeTitre[i]])
                            nombreLiens+=1
                            k+=1

                    fL.write(str(k)+"\n")
                    if nombreLiens>0:
                        for nb in range(nombreLiens):
                            fC.write(str(1/nombreLiens)+"\n")


    def parseCliTolist(self,file_c,file_l,file_i):
        C = open(file_c, "r")
        L = open(file_l, "r")
        I = open(file_i, "r")
        Ct=C.read()
        Lt=L.read()
        It=I.read()
        return Ct,Lt,It


if __name__ == "__main__":
    start_time = time.time()
    dict = Dico(fichierCorpus,fichierMotEnlever)
    dict.nettoyage_texte()
    dict.saveDic("dico.txt")
    dict.genererCLI()
    C,L,I=dict.parseCliTolist("fichierC.txt","fichierL.txt","fichierI.txt")
    m=mcreuz(L, C, I)
    print(m.pagerank_zap())
