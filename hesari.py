#hesarin etusivun otsikot ja ajatusviivojen määrä niissä

#tuo kirjastot
import urllib.request as urllib
import time

#___________Sivun prosessointi__________________
#avataan sivu tarkasteltavaksi
wiki = "http://www.hs.fi/"
page = urllib.urlopen(wiki)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

#etsitään otsikot
h2 = soup.find_all("div", class_="teaser-heading")

#listätään otsikot listaan tab
tab = []
for i in h2:
    #koska otsikkoteksti ei ole suoraan "teaser-heading"-taulukon alla
    #haetaan taulukon alapuolelta otsikot ja talletetaan listaan
    children = i.findChildren()
    for child in children:
        strin = child.get_text()
        tab.append(strin.strip())

#____________Datan prosessointi____________________-
#lasketaan ajatusviivat
lask = 0

for i in tab:
    print(i)
    try:
        i.index("–")
        lask += 1
    except ValueError:
        continue

#otsikkojen määrä yhteensä
otsikoita = len(tab)

#__________Tulosteet ja tallennus___________________
print("\nOtsikoita yhteensä:", otsikoita)
print("Otsikoita joissa väliviiva: ", lask)
print("Osuus: %.2f" % (lask/otsikoita))


#tallennetaan otsikot tiedostoon
tiedostonimi = time.strftime("%d.%m.%Y.") + time.strftime("%H.%M.%S") + ".txt"

#otsikot
f = open(tiedostonimi,'w')
for i in tab:
    f.write(i)
    f.write("\n")

# tulokset
f.write("\n")
f.write(str(otsikoita))
f.write(" Otsikkoa")
f.write("\n")

f.write(str(lask))
f.write(" ajatusviivalla")
f.write("\n")

f.write(str(lask/otsikoita))
f.write("\n")

f.close()




