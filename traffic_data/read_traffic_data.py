import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"

import pandas as pd

# csv file name
filename = '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG.csv'

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

# station
plats_fr = []
platssignatur_fr = []

# number of trains (per type)
#RST	Persontrafik	Tågfärd	Resandetåg
#GT	Godstrafik	Tågfärd	Godståg
#TJT	Tjänstetåg	Tågfärd	Tjänstetåg
#SPF	Godstrafik	Spärrfärd	Vagnuttagning
#VXR	Tjänstetåg	Växling	Växling

antaltåg = {}
antaltåg["RST"] = []
antaltåg["GT"] = []
antaltåg["TJT"] = []
antaltåg["VXR"] = []
antaltåg["SPF"] = []

# traffic density
tåg = []
tågkm = []
tågvikt = []

# genomsnitt
tåglängd_snitt = []
antalvagnar_snitt = []
antalaxlar_snitt = []

# reading csv file
chunk_num = 1
chunksize = 10 ** 6
for chunk in pd.read_csv(filename,chunksize=chunksize,skiprows=1,error_bad_lines=False):
    # extracting field names through first row
    #fields = next(csv_reader)
    # extracting each data chunk one by one  
        # extracting each data row one by one  
    print(chunk_num)
    chunk_num = chunk_num + 1
    for row in chunk.values.tolist():
        row = list(row[0].split(';'))
        if(len(row)<31): # skip if incomplete row
            continue
        if(row[25] == "0.00"): # skip if no rapporterad tågvikt
            continue
        if('J' == row[29]): # skip if train is cancelled
            continue
        # add up the number of trains
        if not (row[13] in plats_fr):
            # initialize location of the station in the lists
            plats_fr.append(row[13])
            platssignatur_fr.append(row[12])
            # initialize number of trains
            antaltåg['RST'].append(0)
            antaltåg['GT'].append(0)
            antaltåg['TJT'].append(0)
            antaltåg['VXR'].append(0)
            antaltåg['SPF'].append(0)
            # init with 1 for the first type of trains
            antaltåg[row[4]][-1] = 1
            # initi traffic intensity
            tåg.append(1)
            tågkm.append(float(row[24]))
            tågvikt.append(float(row[25]))
            # init average characteristics of trains
            tåglängd_snitt.append(float(row[26]))
            antalvagnar_snitt.append(float(row[27]))
            antalaxlar_snitt.append(float(row[28]))
        else:
            # get location in the lists
            loc = plats_fr.index(row[13])
            # increase number of trains
            antaltåg[row[4]][loc] = antaltåg[row[4]][loc]+1
            # increase traffic intensity.
            tåg[loc] = tåg[loc] + 1
            tågkm[loc] = tågkm[loc] + float(row[24])
            tågvikt[loc] = tågvikt[loc] + float(row[25])
            # update average characteristics of trains
            tåglängd_snitt[loc] = tåglängd_snitt[loc] + float(row[26]) #((tåg[loc]-1)*tåglängd_snitt[loc]+float(row[26]))/tåg[loc]
            antalvagnar_snitt[loc] = antalvagnar_snitt[loc] + float(row[27])#((tåg[loc]-1)*antalvagnar_snitt[loc]+float(row[27]))/tåg[loc]
            antalaxlar_snitt[loc] = antalaxlar_snitt[loc] + float(row[28])#((tåg[loc]-1)*antalaxlar_snitt[loc]+float(row[28]))/tåg[loc]


# export to a csv file
rows = zip(plats_fr,platssignatur_fr,antaltåg['RST'],antaltåg['GT'],antaltåg['TJT'],antaltåg['VXR'],antaltåg['SPF'],tåg,tågkm,tågvikt,tåglängd_snitt,antalvagnar_snitt,antalaxlar_snitt)

with open('//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2017/Export_traffic_data.csv','w',newline="") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)