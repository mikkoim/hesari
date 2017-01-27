"""
Skripti hakee Helsingin Sanomien etusivun pääotsikot, laskee niistä ajatusviivat ja tallentaa
tämän tiedon tiedostoon

Mikko Impiö 2017
"""

# tuo kirjastot
import urllib.request as urllib
import time
import tweepy
import schedule
from config import *

class Viivanhakija:

    def __init__(self, url, tunniste):
        self.__data = self.parse(url,tunniste)
        self.__viivoilla = self.process(self.__data)
        self.__otsikoita = len(self.__data)
        self.__osuus = self.__viivoilla/self.__otsikoita

    # ___________Sivun prosessointi__________________
    @staticmethod
    def parse(self,url,otsikkotunniste):
        """
        :param url: tarkasteltavan sivun url-osoite
        :param otsikkotunniste: otsikon erottava tunniste
        """

        # avataan sivu tarkasteltavaksi
        page = urllib.urlopen(url)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page, "html.parser")

        # etsitään otsikot
        h2 = soup.find_all("div", class_=otsikkotunniste)

        # listätään otsikot listaan tab
        tab = []
        for i in h2:
            # koska otsikkoteksti ei ole suoraan "teaser-heading"-taulukon alla
            # haetaan taulukon alapuolelta otsikot ja talletetaan listaan
            children = i.findChildren()
            for child in children:
                strin = child.get_text()
                tab.append(strin.strip())
        return tab

    # ____________Datan prosessointi____________________
    @staticmethod
    def process(self,data):
        """
        :param data: otsikkodata listana
        :return: viivallisten otsikoiden määrä
        :return: otsikoiden kokonaismäärä
        """
        # lasketaan ajatusviivat
        lask = 0

        for i in data:
            try:
                i.index("–")
                lask += 1
            except ValueError:
                continue

        return lask

    # __________Tulosteet ja tallennus___________________
    def tulosta(self):
        """
        Tulostaa otsikot sekä niiden ajatusviivadatan
        """
        for i in self.__data:
            print(i)


        print("\nOtsikoita yhteensä:", self.__otsikoita)
        print("Otsikoita joissa väliviiva: ", self.__viivoilla)
        print("Osuus: %.2f" % (self.__osuus))

    def tallenna(self):
        """
        Tallentaa otsikot ja datan tiedostoon joka on nimetty päivän ja ajan mukaan
        """
        # tallennetaan otsikot tiedostoon
        tiedostonimi = time.strftime("%d.%m.%Y.") + time.strftime("%H.%M.%S") + ".txt"

        # otsikot
        f = open(tiedostonimi,'w')
        for i in self.__data:
            f.write(i)
            f.write("\n")

        # tulokset
        f.write("\n")
        f.write(str(self.__otsikoita))
        f.write(" Otsikkoa")
        f.write("\n")

        f.write(str(self.__viivoilla))
        f.write(" ajatusviivalla")
        f.write("\n")

        f.write(str(self.__osuus))
        f.write("\n")

        f.close()
    def tulostatwiitti(self):
        """
        muotoilee tulokset twiitattavaan muotoon
        :return: twiitti string-muodossa
        """

        """
        twiitti = "Helsingin Sanomien etusivulla on tällä hetkellä {} pääotsikkoa" \
                  " – jopa {:.1f}% ({} kpl) sisältää ajatusviivan. #ajatusviiva @hsfi" \
            .format(self.__otsikoita, float(self.__osuus*100), self.__viivoilla)
        """
        twiitti = str(time.strftime("%H.%M.%S")) + ": {}, {:.1f}, {}" \
            .format(self.__otsikoita, float(self.__osuus*100), self.__viivoilla)
        return twiitti

def twitter(etusivu):
    """
    kommunikoi twitter API:n kanssa ja twiittaa tulokset
    :param etusivu: viivanhakija-luokka johon on prosessoitu tämänhetkinen etusivu
    :return:
    """

    #autentikoinititiedot haetaan config.py-tiedostosta
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    #päivittää statuksen
    api.update_status(etusivu.tulostatwiitti())


def job():
    """
    kahdesti päivässä suoritettava funktio, joka:
    -Hakee etusivun
    -Prosessoi sen
    -Twiittaa tulokset
    -Tallentaa tulokset tiedostoon
    """
    URL = "http://www.hs.fi/"
    OTSIKKOTUNNISTE = "teaser-heading"

    #prosessoi etusivun ja luo olion
    etusivu = Viivanhakija(URL, OTSIKKOTUNNISTE)

    #twiittaa etusivun tiedot
    twitter(etusivu)

    #etusivu.tulosta()
    #tallentaa etusivun tiedostoon
    etusivu.tallenna()


def main():

    schedule.every().day.at("00:40").do(job)
    schedule.every().day.at("01:00").do(job)
    schedule.every().day.at("02:00").do(job)
    schedule.every().day.at("03:00").do(job)
    schedule.every().day.at("04:00").do(job)
    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("15:00").do(job)
    schedule.every().day.at("18:00").do(job)
    schedule.every().day.at("20:00").do(job)


    while True:
        schedule.run_pending()
        time.sleep(1)

main()
