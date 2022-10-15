import csv

# dict={}
# csvFile = open('locations_mapped.csv', 'a', encoding="utf-8",newline='')
# csvWriter = csv.writer(csvFile)
#
# with open('../Data_url/location_source.csv',encoding="utf-8") as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',')
#     for row in spamreader:
#         dict[row[0]]=row[1]
#
# with open('../location.csv', newline='',encoding="utf-8") as csvfile:
#      spamreader = csv.reader(csvfile, delimiter=',')
#      for row in spamreader:
#          if row[1] in dict:
#              row[4]=dict[row[1]]
#          csvWriter.writerow(row)

csvFile = open('hotels_mapped.csv', 'a', encoding="utf-8",newline='')
csvWriter = csv.writer(csvFile)

with open('../hotel.csv', newline='',encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        row[0]=row[0].replace("\r\n"," ")
        row[0]=row[0].replace("\n"," ")
        csvWriter.writerow(row)


