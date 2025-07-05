class IVistockVnDirectScraper:
    def fetch(self, url: str):
        ...

class AsyncIVistockVnDirectScraper:
    async def async_fetch(self, url: str):
        ...

class IVistock24HMoneyScraper:
    def fetch(self, url: str):
        ...

class AsyncIVistock24HMoneyScraper:
    async def async_fetch(self, url: str):
        ...