import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"

import pandas as pd

# csv file name
filename = '//vti.se/root/Mistrainfra/Data/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG.csv'

# small sample (for testing)
#filename = '//vti.se/root/Mistrainfra/Data/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG_0.csv'
  
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

# station (from)
plats_fr = "Kimstad" # Kimstad

# number of trains (per type)
#RST	Persontrafik	Tågfärd	Resandetåg
#GT	Godstrafik	Tågfärd	Godståg
#TJT	Tjänstetåg	Tågfärd	Tjänstetåg
#SPF	Godstrafik	Spärrfärd	Vagnuttagning
#VXR	Tjänstetåg	Växling	Växling

# reading csv file
chunk_num = 1
chunksize = 10 ** 6

with open('//vti.se/root/Mistrainfra/Data/Trafikdata 2017/Export_traffic_data_Kimstad.csv','w',newline="") as f:
    writer = csv.writer(f)

for chunk in pd.read_csv(filename,chunksize=chunksize,skiprows=1,error_bad_lines=False):
    # create output csv file
    with open('//vti.se/root/Mistrainfra/Data/Trafikdata 2017/Export_traffic_data_Kimstad.csv','a',newline="") as f:
        writer = csv.writer(f)
    # extracting field names through first row
    #fields = next(csv_reader)
    # extracting each data chunk one by one  
        # extracting each data row one by one  
        print(chunk_num)
        chunk_num = chunk_num + 1
        for row in chunk.values.tolist():
            row = list(row[0].split(';'))
            if(len(row)<31):
                continue
            # if train is cancelled
            if('J' == row[29]):
                continue
            # add up the number of trains
            if row[12] == plats_fr:
                writer.writerow(row)