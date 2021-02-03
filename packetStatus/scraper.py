from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self, **kwargs):
        self.__objeto = kwargs["objeto"]
        self.__URL = None

        self.log = []

    @abstractmethod
    def check_new_info(self): raise NotImplementedError

    def set_tracking_url(self, URL):
        self.__URL = URL

    @property
    def URL(self): return self.__URL

    @property
    def objeto(self): return self.__objeto
