#hesarin etusivun otsikot ja ajatusviivojen määrä niissä

#tuo kirjastot
import urllib.request as urllib
import time

#avataan sivu tarkasteltavaksi
wiki = "http://www.hs.fi/"
page = urllib.urlopen(wiki)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

#etsitään otsikot
h2 = soup.find_all("h2")

#listätään otsikot listaan
tab = []
for i in h2:
    strin = i.get_text()
    tab.append(strin)

# poistetaan listasta turhat välilyönnit
stripped = []
for otsikko in tab:
    strip = otsikko.strip()
    stripped.append(strip)

# poistetaan lopun ei-otsikot
montako_otsikkoa = len(stripped)-18
stripped = stripped[:montako_otsikkoa]

#lasketaan ajatusviivat
lask = 0
for i in stripped:
    print(i)
    try:
        i.index("–")
        lask += 1
    except ValueError:
        continue

#välissä on kolme ei-otsikkoa yleensä
otsikoita = len(stripped)-3

#tulosteet
print("\nOtsikoita yhteensä:", otsikoita)
print("Otsikoita joissa väliviiva: ", lask)
print("Osuus: %.2f" % (lask/otsikoita))


#tallennetaan otsikot tiedostoon
tiedostonimi = time.strftime("%d.%m.%Y") + ".txt"

#otsikot
f = open(tiedostonimi,'w')
for i in stripped:
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









