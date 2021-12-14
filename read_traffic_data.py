import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"

import pandas as pd

# csv file name
filename = '//vti.se/root/Mistrainfra/Data/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG.csv'
  
# initializing the titles and rows list and line counter
# col 1 - tåguppdrag
# col 2 - tågnr
# col 3  {"Tågordning uppdrag", Int64.Type}
# col 4 - {"Datum (PAU)", type date}
# col 5 - {"Tågslag", type text}
# col 6 - {"UppehållstypAvgång", type text}
# col 7 - {"UppehållstypAnkomst", type text}
# col 8 - {"Delsträckanummer", Int64.Type}
# col 9 - {"Första platssignatur", type text}
# col 10 - {"Första platssignatur för uppdrag", type text}
# col 11 - {"Sista platssignatur", type text}
# col 12 - {"Sista platssignatur för uppdrag", type text}
# col 13 - {"Avgångsplats", type text}
# col 14 - {"Från platssignatur", type text}
# col 15 - {"Ankomstplats", type text}
# col 16 - {"Till platssignatur", type text}
# col 17 - {"Sträcka med riktning", type text}
# col 18 - {"Inställelseorsakskod", type text}
# col 19 - {"Inställelseorsak", type text}, 
# 20 {"Ankomsttid", type text}, 
# 21 {"Avgångstid", type text}
# 22 {"Planerad ankomsttid", type datetime}, 
# 23 {"Planerad avgångstid", type datetime}, 
# 24 {"Dragfordonsid", type text}, 
# 25 {"Framförda tågkm", type text}, 
# 26 {"Rapporterad tågvikt", type text}, 
# 27 {"Rapporterad tåglängd", type text}, 
# 28 {"Antal rapporterade vagnar", Int64.Type}, 
# 29 {"Antal rapporterade hjulaxlar", Int64.Type}, 
# 30 {"Inställtflagga", type text},
# 31 {"Planeringsstatus", type text}})

fields = []
set_tågnr = set()
dict_delsträckor = dict()

nb_trains = 0

# reading csv file

chunksize = 10 ** 6
for chunk in pd.read_csv(filename,chunksize=chunksize, skiprows = 1,error_bad_lines=False):
    # extracting field names through first row
    #fields = next(csv_reader)
    # extracting each data chunk one by one  
        # extracting each data row one by one  
    #print(chunk)
    for row in chunk.values.tolist():
        row = list(row[0].split(';'))
        # add up the number of trains
        if not (row[1] in set_tågnr):
            nb_trains = nb_trains + 1
            set_tågnr.add(row[1])
        # add up the number of trains per link
        if (row[13], row[15]) in dict_delsträckor:
            dict_delsträckor[(row[13], row[15])] = dict_delsträckor[(row[13], row[15])] + 1
        else:
            dict_delsträckor[(row[13], row[15])] = 1
print('Number of trains: ' + nb_trains)
print('Size of set of trains: ' + len(set_tågnr))
print('Number of trains over link btw Karlberg/Ke -> Stockholm/Cst ' + dict_delsträckor[('Ke','Cst')])