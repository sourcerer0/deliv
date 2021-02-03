from bs4 import BeautifulSoup
from .locator import GPS
import requests

class CEP_LOCATOR(GPS):
    def __init__(self):
        super().__init__()
        self.__URL = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm"
        self.__CEP = None
        self.__ADDRESS = None

    def set_address(self):
        results_list = []
        CEP_code = input("Enter your CEP code:\n")
        self.set_CEP(CEP_code)
        reply = requests.post(self.__URL, data={"relaxation": self.__CEP})
        if reply.ok:
            soup = BeautifulSoup(reply.text, "html.parser")
            result = soup.find_all("table", class_="tmptabela")
            result = result[0].find_all("td")
            for i in result:
                opentag_parsed = str(i).split("<")
                closetag_parsed = opentag_parsed[1].split(">")
                results_list.append(closetag_parsed[1].encode("utf-8", "ignore"))
            location = ", ".join(results_list)
        self.__ADDRESS = location
    def get_address(self):
        return self.__ADDRESS
    ADDRESS = property(fget=get_address)

    def set_CEP(self, value):
        try:
            CEP_code = int(value)
        except ValueError:
            print("CEP must be a number!")
            return
        self.__CEP = CEP_code
    def get_CEP(self):
        return self.__CEP
    CEP = property(fget=get_CEP)
