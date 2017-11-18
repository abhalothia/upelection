import csv

myData = [['Name', 'Father/Mother', 'Age'], ['Name', 'Father/Mother', 'Age'], ['Name', 'Father/Mother', 'Age']]
csv.register_dialect('myDialect', quoting=csv.QUOTE_NONE)

myFile = open('csvexample4.csv', 'w')  
with myFile:  
   writer = csv.writer(myFile)
   writer.writerows(myData)