import threading
import time
from ExcelManager import ExcelManager

class ThreadManager (threading.Thread):
    def __init__(self, filename, of):
        threading.Thread.__init__(self)
        self.filename = filename
        self.of = of
        self.compteur = 0
        self.execution_time = 0
    
    def run(self):
        manager = ExcelManager(self.filename)
        start_time =time.time()
        manager.run(self.of)
        self.execution_time = time.time() - start_time
        self.compteur = int(manager.get_compteur())

    def get_compteur(self):
        return self.compteur

    def get_execution_time(self):
        return self.execution_time
