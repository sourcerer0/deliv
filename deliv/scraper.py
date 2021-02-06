from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self, **kwargs):
        """
        Parameters:
            kwargs['data'] (string): Data
        """
        self.__data = kwargs["data"]
        self.__URL = None

        self.log = []

    @abstractmethod
    def check_new_info(self): raise NotImplementedError

    def set_tracking_url(self, URL):
        self.__URL = URL

    @property
    def URL(self): return self.__URL

    @property
    def data(self): return self.__data
