from bs4 import BeautifulSoup
import requests

from .scraper import Scraper

class Cep(Scraper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__ADDRESS = None
        self.set_tracking_url(
            "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm")

    def check_new_info(self):
        info = []
        reply = requests.post(self.URL, data={"relaxation": self.objeto})

        for _ in range(10):
            if reply.ok:
                soup = BeautifulSoup(reply.text, "html.parser")
                result = soup.find_all("table", class_="tmptabela")
                result = result[0].find_all("td")

                for i in result:
                    opentag_parsed = str(i).split("<")
                    closetag_parsed = opentag_parsed[1].split(">")
                    info.append(closetag_parsed[1].encode("utf-8", "ignore"))

                self.address = ", ".join(info)
                return info

            else: continue
        print("ERROR ****** ********\nRequest timeout! ******")
        return info


    @property
    def address(self): return self.__ADDRESS

    @address.setter
    def address(self, addr): self.__ADDRESS = addr
