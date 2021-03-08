import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
import re

class Corpus:

    RACINE = '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="fr">'
    PREF = '{http://www.mediawiki.org/xml/export-0.10/}'
    NBPAGE = 5000

    def __init__(self, name_file = None,motRemove="motExit.xml", key_words = ['musique', 'cinéma', 'artiste','acteur','actrice'], out_file = "wiki_musique.xml", corpusFile="corpusfile.xml"):
        self.name_file = name_file
        self.key_words = key_words
        self.out_file = out_file
        self.motRemove=motRemove
        self.corpusFile=corpusFile

    def netoyage(self):
        i = 0
        with open(self.out_file, 'w') as o:
            o.write(self.RACINE)
            for event, elem in ET.iterparse(self.name_file):
                if elem.tag == self.PREF+'page':
                    txt = elem.find(self.PREF+'revision/'+self.PREF+'text').text
                    if txt:
                        ajout=False
                        for mot in self.key_words:
                            if not ajout:
                                if mot in txt.lower():
                                    elemstr = ET.tostring(elem, encoding="unicode", method="xml")
                                    o.write(elemstr)
                                    i += 1
                                    ajout=True
                                    print(i)

                                    #s'arreter à NBPAGE pages
                                    if i == self.NBPAGE:
                                        break


            o.write('</mediawiki>')
            print('SUCCESS')

    def formatage(txt2):
        return txt2

"""
    def nettoyage_texte(self):
        dic={}
        stop_wordsFrench = set(stopwords.words('french'))
        for line in open(self.motRemove,'r'):
            for mot in line.split():
                stop_wordsFrench.add(mot)
        numberPage=0
        with open(self.corpusFile, 'w') as o:
            o.write(self.RACINE)
            for event, elem in ET.iterparse(self.out_file):
                if elem.tag == self.PREF+'page':
                    elemstr = ET.tostring(elem, encoding="unicode", method="xml")


                    elemstr = re.sub('((url=https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)(?:com|net|org|edu|gov|fr|php)', ' ',elemstr) # les balises
                    elemstr = re.sub('((url=http?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)(?:com|net|org|edu|gov|fr|php)', ' ',elemstr)
                    elemstr = re.sub('((url=https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', ' ',elemstr)
                    elemstr = re.sub('((url=http?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', ' ',elemstr)

                    o.write(elemstr)
                    numberPage+=1
                    print(numberPage)
"""



if __name__ == "__main__":
    cpus = Corpus('frwiki10000.xml')
    cpus.netoyage()

    #cpus.nettoyage_texte();
