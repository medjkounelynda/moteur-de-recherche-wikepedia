"""
Created on Sat Jan  9 18:56:20 2021

@author: Soumeya
"""

from lxml import etree
import re
import unidecode


#------------------------------------------------------------------------
#fonction pour sélectionner un ensemble de pages du thème choisi

def SelectTheme(theme,page):
    if theme in page:
         return True
    else:
        return False

#-------------------------------------------------------------------------
def dictMots(dict,textPage,idPage):
    stoplist=['la','le','d','est','tres','un','qui','de','faire','pour','selon','son','en','il','sur','ou','des','entre','et','une','du']
    t=textPage.lower()
    t = re.sub(r"'", " ",t)
    t = re.sub('\s+','  ',t)
    t = re.sub('<[^>]+>|\[\[?|\]\]?|\{\{|\}\}|\||:|=+|\W|([0-9]{1,3})', ' ',t)
    t=t.split()


    for w in t:
        #print(w)
        l=[]
        li=[]
        if (not w in stoplist and len(w)>1):
            if (not w in dict):
                l.append(idPage)
                dict[w]=l
                l=[]

            else:
                li=dict[w]
                if(not idPage in li):
                   li.append(idPage)
                   dict[w]=li
                   li=[]
    return dict
#--------------------------------------------------------------------------
def parseMethode(fichier):

  tree = etree.parse(fichier)
  root = tree.getroot()
  element = root[0]
  root1 = etree.Element("mediawiki")
  count=0
  dict={}
  dictPage={}


  for page in root.findall('{http://www.mediawiki.org/xml/export-0.10/}page'):
      title = page.find('{http://www.mediawiki.org/xml/export-0.10/}title')
      id = page.find('{http://www.mediawiki.org/xml/export-0.10/}id')
      revision=page.find('{http://www.mediawiki.org/xml/export-0.10/}revision')
      texte= revision.find('{http://www.mediawiki.org/xml/export-0.10/}text')
      att1=texte.get('bytes')
      textNet=texte.text
      texte.set('attribute_name', 'attribute_value')
      textNet=textNet.split("== Notes et références ==")[0]

      textNet = re.sub(r"\s*{.*?}}\s*", " ",textNet)
      textNet=unidecode.unidecode(textNet)


      if (SelectTheme("Antoine",title.text)):

         page1 = etree.SubElement(root1, "page")
         etree.SubElement(page1, "title").text=title.text
         etree.SubElement(page1, "id").text = id.text
         etree.SubElement(page1, "text",{"bytes": att1},space="preserve").text = textNet

         textPage=title.text +" "+ textNet
         idPage=id.text
         #print("textPage ",textPage)
         dictPage=dictMots(dict,textPage,idPage)
         dict=dictPage
  dict=sorted(dict.items(), key=lambda x: x[0])
  print(dict)


  tree = etree.ElementTree(root1)
  tree.write("fichierNet.xml",encoding="UTF-8",pretty_print=True)

print( parseMethode("frwiki10000.xml"))
