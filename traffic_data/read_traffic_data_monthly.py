import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"
import datetime

import pandas as pd

# csv file name
filename = [\
#    '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG_0.csv',\
        '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2015/VTI_20150101_20151231_TrafikJVG.csv', \
    '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2016/VTI_20160101_20161231_TrafikJVG.csv',\
    '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2017/VTI_Rådata20170101_20171231_TrafikJVG.csv',\
    '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2018/VTI_Rådata20180101_20181231_TrafikJVG.csv']
#filename = 
#filename = 
#filename = 


# small sample (for testing)
#
  
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

# reading csv file
for fil_id in range(0,4):

    # station
    plats_fr = []
    månad = []
    år = fil_id

    # number of trains (per type)
    #RST	Persontrafik	Tågfärd	Resandetåg
    #GT	Godstrafik	Tågfärd	Godståg
    #TJT	Tjänstetåg	Tågfärd	Tjänstetåg
    #SPF	Godstrafik	Spärrfärd	Vagnuttagning
    #VXR	Tjänstetåg	Växling	Växling

    antaltåg_medvikt = {'RST': [], 'GT': [], 'TJT': [], 'VXR': [], 'SPF': []}

    antaltåg_ingenvikt ={'RST': [], 'GT': [], 'TJT': [], 'VXR': [], 'SPF': []}

    # traffic density
    tågkm = {'RST': [], 'GT': [], 'TJT': [], 'VXR': [], 'SPF': []}
    tågvikt = {'RST': [], 'GT': [], 'TJT': [], 'VXR': [], 'SPF': []}

    # genomsnitt
    #tåglängd_snitt = []
    #antalvagnar_snitt = []
    #antalaxlar_snitt = []


    chunk_num = 1
    chunksize = 10 ** 6
    for chunk in pd.read_csv(filename[fil_id],chunksize=chunksize,skiprows=1,error_bad_lines=False):
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
            if('J' == row[29]): # skip if train is cancelled
                continue
            if(row[20]=="Saknas     -    "): # skip if no depature time
                continue
            # get the month of the (actual) departure
            datem = datetime.datetime.strptime(row[20], "%Y-%m-%d %H:%M")
            #pls_mån = row[13]+str(datem.month)
            
            # add up the number of trains
            if not (row[13] in plats_fr): #or not (pls_mån in id_plats_fr[row[13] in plats_fr]):
                # initialize location of the station in the lists
                plats_fr.append(row[13])
                
                # initialize number of trains for the driftplats
                for key in antaltåg_medvikt:
                    antaltåg_medvikt[key].append([int(0)]*12)
                    antaltåg_ingenvikt[key].append([int(0)]*12)
                    tågkm[key].append([.0]*12)
                    tågvikt[key].append([.0]*12)

                if(row[25] == "0.00"): # if no rapporterad tågvikt
                    antaltåg_ingenvikt[row[4]][-1][datem.month-1] = int(1)
                else:
                    antaltåg_medvikt[row[4]][-1][datem.month-1] = int(1)

                tågvikt[row[4]][-1][datem.month-1] = float(row[25])
                tågkm[row[4]][-1][datem.month-1] = float(row[24])

                # init average characteristics of trains
                #tåglängd_snitt.append([range(0,12)*0])
                #tåglängd_snitt[datem.month-1][-1] = float(row[26])
                #antalvagnar_snitt.append([range(0,12)*0])
                #antalvagnar_snitt[datem.month-1][-1] = float(row[27])
                #antalaxlar_snitt.append([range(0,12)*0])
                #antalaxlar_snitt[datem.month-1][-1] = float(row[28])
            else:
                # get location in the lists
                loc = plats_fr.index(row[13])
                # increase number of trains
                if(row[25] == "0.00"): # if no rapporterad tågvikt
                    antaltåg_ingenvikt[row[4]][loc][datem.month-1] = antaltåg_ingenvikt[row[4]][loc][datem.month-1]+int(1)
                else:
                    antaltåg_medvikt[row[4]][loc][datem.month-1] = antaltåg_medvikt[row[4]][loc][datem.month-1]+int(1)
                # increase traffic intensity.
                tågkm[row[4]][loc][datem.month-1]= tågkm[row[4]][loc][datem.month-1] + float(row[24])
                tågvikt[row[4]][loc][datem.month-1] = tågvikt[row[4]][loc][datem.month-1] + float(row[25])
                # update average characteristics of trains
                #tåglängd_snitt[loc] = tåglängd_snitt[loc] + float(row[26]) #((tåg[loc]-1)*tåglängd_snitt[loc]+float(row[26]))/tåg[loc]
                #antalvagnar_snitt[loc] = antalvagnar_snitt[loc] + float(row[27])#((tåg[loc]-1)*antalvagnar_snitt[loc]+float(row[27]))/tåg[loc]
                #antalaxlar_snitt[loc] = antalaxlar_snitt[loc] + float(row[28])#((tåg[loc]-1)*antalaxlar_snitt[loc]+float(row[28]))/tåg[loc]



    with open('//vti.se/root/Mistrainfra/Data/Trafikdata/Export_traffic_data_'+str(2015+fil_id)+'.csv','w',encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        # export to a csv file
        hdr = ['plats_fr','månad','antaltåg_medvikt_RST','antaltåg_medvikt_GT','antaltåg_medvikt_TJT','antaltåg_ingenvikt_RST',\
            'antaltåg_ingenvikt_GT','antaltåg_ingenvikt_TJT','tågkm_RST','tågkm_GT','tågkm_TJT','tågvikt_RST','tågvikt_GT','tågvikt_TJT']
        writer.writerow(hdr)
        for id in range(0,len(plats_fr)):            
            rows = zip([plats_fr[id]]*12,range(1,13),antaltåg_medvikt['RST'][id],antaltåg_medvikt['GT'][id],antaltåg_medvikt['TJT'][id],\
                antaltåg_ingenvikt['RST'][id],antaltåg_ingenvikt['GT'][id],antaltåg_ingenvikt['TJT'][id],\
                tågkm['RST'][id],tågkm['GT'][id],tågkm['TJT'][id],\
                tågvikt['RST'][id],tågvikt['GT'][id],tågvikt['TJT'][id])
            for row in rows:
                writer.writerow(row)