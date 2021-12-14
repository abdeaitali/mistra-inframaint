import csv

# csv file name
filename = '//vti.se/root/Mistrainfra/Data/som CSV/Infrafel_och_tågstörande_fel_2016-2017.csv'
  
# initializing the titles and rows list and line counter
fields = []
rows_rail = []
rows_switche = []
line_count = 1

# reading csv file
with open(filename, 'r', encoding="utf8") as csv_file:
    # creating a csv reader object
    csv_reader = csv.reader(csv_file, delimiter=';')
    # extracting field names through first row
    fields = next(csv_reader)
    # extracting each data row one by one  
    for row in csv_reader:
        if line_count == 5:
            break
        elif row[21] == "Spårväxel":
            rows_switche.append([row[7],row[9],row[10],row[11],row[12],row[13]])
        elif row[21] == "Spår":
            rows_rail.append([row[7],row[9],row[10],row[11],row[12],row[13]])
        else:
            continue    
    print(f'Processed {line_count} lines.')