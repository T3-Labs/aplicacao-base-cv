from PyQt5.QtCore import QThread
import schedule
import requests

class DataIter(QThread):

    def __init__(self) -> None:
        super().__init__()
        self.apiURL = "http://localhost:8000/api/v1/client/criar/"
        self.payload = dict()
        #Futuramente colocar como uma variável de ambiente (.env)

    @staticmethod
    def make_payload():
        payload = dict()
        payload["line"] = int
        payload["parts_quantity"] = int
        payload["area_production"] = float
        payload["line_stops"] = bool
        payload["stops_quantity"] = list
        return payload

    def insert_data(self, data: dict):
        self.payload = self.make_payload()
        self.payload["line"] = data["line"]
        self.payload["parts_quantity"] = data["parts_quantity"]
        self.payload["area_production"] = data["area_production"]
        self.payload["line_stops"] = data["line_stops"]
        self.payload["stops_quantity"] = data["stops_quantity"]

    def send_payload(self):
        url = self.apiURL
        payload = self.payload
        try:
            sucess = requests.post(url, json=payload, timeout=(2, 2))
            return sucess
        except Exception as e:
            print(f"Logger: Resquests post failed - {e}")
            return False

    def run(self):
        schedule.every(1).minutes.do(self.send_payload)
        while not self.isInterruptionRequested:
            schedule.run_pending()
            

    def __del__(self):
        schedule.clear()
        self.requestInterruption()
        self.wait()

#Comunica com o Banco de Dados

