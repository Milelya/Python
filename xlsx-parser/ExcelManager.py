
import openpyxl as pyxl

class ExcelManager():
    def __init__(self, filePath):
        self.file_path = filePath
        self.compteur = 0
    
    def get_compteur(self):
        return self.compteur

    def reset_compteur(self):
        self.compteur = 0
    
    def run(self, of):
        wb = pyxl.load_workbook(self.file_path, read_only=True)
        ws = wb.active
        of = str(of)
        compteur = 0
        relay = 0
        compteur_tempo = 0
        emptyCounter = 0
        for row in ws.iter_rows(min_col=4, max_col=16):
            column_counter = 0
            for cell in row:
                if of in str(cell.value):
                    relay = 1

                if relay and column_counter == 1 :
                    compteur_tempo = int(cell.value)

                if relay and column_counter == 12:
                        if cell.value is None:
                            compteur = compteur + compteur_tempo
                        compteur_tempo = 0
                        relay = 0
                column_counter = column_counter + 1

                if cell.value is None :
                    emptyCounter = emptyCounter + 1
                else :
                    emptyCounter = 0
            if emptyCounter > 100000 :
                break
        
                
                    

        self.compteur = compteur
        wb.close()
