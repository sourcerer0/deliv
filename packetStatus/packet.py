from bs4 import BeautifulSoup
import requests

from abc import ABC, abstractmethod


class Packet(ABC):
    def __init__(self, objeto, **kwargs):
        self.__objeto = objeto
        self.__URL = None

        self.log = []

    @abstractmethod
    def check_new_info(self): raise NotImplementedError

    @abstractmethod
    def set_tracking_url(self, URL):
        # ADD SUPPORTED PLATFORMS
        self.__URL = URL

    @property
    def URL(self): return self.__URL

    @property
    def objeto(self): return self.__objeto


class Correios(Packet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_tracking_url(
            "https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm")

    def check_new_info(self):
        info = []
        reply = requests.post(self.URL, data={"objetos": self.objeto})

        for _ in range(10):
            if reply.ok:
                soup = BeautifulSoup(reply.text, "html.parser")
                results = soup.find_all("td", class_="sroLbEvent")

                if len(results) > len(self.log):
                    for i in results:
                        self.log.append(i.text)
                    new_data = len(results) - len(self.log)
                    info = self.log[-new_data:]
                elif len(results) == len(self.log):
                    print("0 new notifications")

                return info

            else: continue
        print("ERROR ****** ********\nRequest timeout! ******")
        return info
