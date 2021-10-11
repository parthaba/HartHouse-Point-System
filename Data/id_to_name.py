import random
import csv

# csv file name
filename = "Debaters/id_list.csv"

# field names
fields = ['Name', 'ID']

# List of members in the club
member_list = ['Amin Ali',
               'Angelina Gao',
               'Anna Clark',
               'Boomba Nishikawa',
               'Charlize Hurley Medina',
               'Ciara McGarry',
               'Daniel Zheng',
               'David Osose Osage Okojie',
               'Dihan Niloy',
               'Eden Zorne',
               'Elgin Lin',
               'Emily Downing',
               'Faadil Butt',
               'Fatema Nami',
               'Ian Lavine',
               'Isabella Li',
               'Isabelle Feng',
               'Jacob Li',
               'Arpi Yang',
               'Justin Dylan Lim',
               'Kristy Lee',
               'Kate Kwon',
               'Khanak Gupta',
               'Lusayo Simwaka',
               'Megan Horsthuis',
               'Mosab Anwary',
               'Mia Feldman',
               'Natalia Manjarres',
               'Nishtha Kawatra',
               'Olivia Sun',
               'Para Bauharan',
               'Rena Wang',
               'Rocco Ruan',
               'Sam Lehman',
               'Samantha Van Der Beek',
               'Samuel Tang',
               'Serena Yuan',
               'Serina Zheng',
               'Sheldon Stern',
               'Silvia Margarian',
               'Sol Kim',
               'Tanvir Shahriar',
               'Terry Luan',
               'Tianchang (Kerry) Li',
               'Tyson Dennis-Sharma',
               'Valerie Pang',
               'Victoria Liu',
               'Zaiboon Azhar',
               'Zara Lal',
               'Adam Banihani',
               'Adrienne Roc',
               'Ahmed Moselhi',
               'Aida Zarghami',
               'Aishwarya Patel',
               'Alexander Kiszely',
               'Amalie Wilkinson',
               'Ameen Parthab',
               'Arya Rahmani',
               'Ashley Costa',
               'Ceylan Borgers',
               'Chris Pang',
               'Deborah Wong',
               'Dhananjay Ashok',
               'Eric Zhao',
               'Gautier Boyrie',
               'Georgia Samuel',
               'Hui Wen Zheng',
               'Jeffrey Ma',
               'Katelyn Wang',
               'Kieran KA',
               'Malcolm Bainborough',
               'Maria Bon',
               'Matt Aydin',
               'Nadia Gericke',
               'Navin Kariyawasam',
               'Nikitha James',
               'Noah Pinno',
               'Rudra Patel',
               'Saara Meghji',
               'Sarah Rana',
               'Sarah Zelifan',
               'Simren Sharma',
               'Taha Syed',
               'Wan Li',
               'Zuha Tanweer'
               ]
member_list.sort()

# list of unique identifiers
id_number_list = random.sample(range(0, 999999), 85)

# data rows of the CSV file
rows = []
for x in range(len(member_list)):
    new_row = [member_list[x], id_number_list[x]]
    rows.append(new_row)

with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csv_writer = csv.writer(csvfile)

    # writing the fields
    csv_writer.writerow(fields)

    # writing the data rows
    csv_writer.writerows(rows)
