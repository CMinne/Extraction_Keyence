import time, os
import pyodbc
import webbrowser
from os import listdir
from os.path import isfile, join


class GetKeyence():
    def __init__(self, *args, **kwargs):

        try: 
            SQL_ATTR_CONNECTION_TIMEOUT = 113
            login_timeout = 1
            connection_timeout = 3
            self.conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                       'Server=SERV27\JTEKT;'
                                       'Database=Plc_prod;'
                                       'UID=quagate;'
                                       'PWD=qua+gate;'
                                       'Trusted_Connection=No;',
                                timeout = login_timeout, attrs_before = {SQL_ATTR_CONNECTION_TIMEOUT : connection_timeout}
                                )
            self.conn.timeout = 3
            self.cursor = self.conn.cursor()
            print("QA SQL Connection : OK")
            self.loop()
        except:
            self.cursor = None
            print("QA SQL Connection impossible")
    def loop(self):
        while(True):
            time.sleep(5)
            id = None
            text = None
            sql = """\
                            SELECT TOP(1) idKeyence, reference, currentOF
                            FROM [Plc_prod].[dbo].[QAGATE_1_KeyenceData]
                            WHERE doubleTaillage IS NULL AND 
	                              coupDenture1 IS NULL AND 
	                              coupDenture2 IS NULL AND
	                              chanfrein1 IS NULL AND
	                              chanfrein2 IS NULL AND
	                              chanfrein3 IS NULL AND
	                              chanfrein4 IS NULL
                        """
            self.cursor.execute(sql)
            val = self.cursor.fetchall()

            for row in val:
                id = row.idKeyence
                reference = row.reference
                of = row.currentOF

            if(id == None):
                continue

            path = '''//SERV14/Public/zzz_Exchange/JPIJER/Fichiers Charly/cv-x/result/SD1_00'''

            if(reference == '490035-2000'):
                ref = '6'
            elif(reference == '490035-2100'):
                ref =  '7'
            elif(reference == '490035-3200'):
                ref =  '8'
            elif(reference == '490035-3300'):
                ref =  '9'

            path += ref

            onlyfiles = [f for f in listdir(os.path.normpath(path))]

            for t in onlyfiles:
                text = t

            if(text == None):
                continue

            time.sleep(5)

            with open(os.path.normpath(path + '/' + text), 'r') as f:
                lines = f.read().splitlines()
                f.close()

            os.remove(os.path.normpath(path + '/' + text))

            last_line = lines[-1]
            data = last_line.split(",")

            sql = """\
                        UPDATE [dbo].[QAGATE_1_KeyenceData] 
                        SET doubleTaillage = ?, coupDenture1 = ?, coupDenture2 = ?, chanfrein1 = ?, chanfrein2 = ?, chanfrein3 = ?, chanfrein4 = ? 
                        WHERE idKeyence = ?
                    """
            self.cursor.execute(sql, data[0], data[1], data[2], data[3], data[4], data[5], data[6], id)
            self.conn.commit()

            continue


def main():

    root = GetKeyence()

if __name__ == '__main__':
    main()

