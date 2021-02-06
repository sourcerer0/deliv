from bs4 import BeautifulSoup
import requests

from .scraper import Scraper
from .location import Location

class Cep(Scraper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__address = Location

        self.set_tracking_url(
            "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm")

    def check_new_info(self):
        info = []
        reply = requests.post(self.URL, data={"relaxation": self.data})

        for _ in range(10):
            if reply.ok:
                soup = BeautifulSoup(reply.text, "html.parser")
                result = soup.find_all("table", class_="tmptabela")[0].find_all("td")

                for i in result:
                    parse = str(i).split("<")[1].split(">")
                    info.append(parse[1].encode("utf-8", "replace").decode("utf-8"))

                del(info[-1])
                self.__address = self.__address(", ".join(info))
                return info

            else: continue
        print("ERROR ****** ********\nRequest timeout! ******")
        return info


    @property
    def address(self): return self.__address
