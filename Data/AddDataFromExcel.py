import csv

import pandas as pd
from Data.AddEntry import AddEntry
from Data.AddEntry import match_id_to_name
from Data.AddDebater import AddDebater


def find_ID(name: str) -> int:
    """Given a username, find the user ID."""
    with open("Debaters/id_list.csv", 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        row_number = 1
        for row in csv_reader:

            # filters out empty rows
            if row_number % 2 == 1:

                # Return the name of the debater with the given debater ID
                if row[0] == str(name):
                    return int(row[1])

            row_number += 1

        print(name)
        print("no user with the name" + name + ", creating a new user.")
        return create_new_user(name)


class ExcelReader:
    """Reads rows from an excel sheet and uploads them to the respective JSON file."""

    df = pd.read_excel(r'C:\Users\james\OneDrive\Desktop\Points Coordinator\Fall 2021.xlsx',
                       sheet_name='Points Tracking')

    def __init__(self):
        """Initialize the ExcelReader."""

    def add_tournament_data(self):
        """Takes in data from excel spreadsheet for debate tournament results and adds them as competitive points."""

        for x in range(len(self.df['Name'])):
            debater_name = self.df.loc[x]['Name']
            semester = "Fall 2021"
            debater_id = find_ID(debater_name)
            new_entry = AddEntry(debater_id, semester)

            tournament_tier = self.df.loc[x]['Tier']
            tournament_name = self.df.loc[x]['Tournament']
            judging = self.df.loc[x]['Judging']

            if judging == 'Yes':
                if self.df.loc[x]['Judge Break'] == 'Yes':
                    break_judge = True
                else:
                    break_judge = False

                new_entry.tournament_judging(tournament_tier, tournament_name, break_judge)

            else:
                size = self.df.loc[x]['No. of Teams']
                team_place = self.df.loc[x]['Team Place']
                speaker_place = self.df.loc[x]['Speaker Place']
                new_entry.tournament_debating(tournament_tier, tournament_name, size, team_place, speaker_place)

    def check_name_to_id(self) -> bool:
        """Check if the name and ID match. If not, print the occurrence."""
        for x in range(len(self.df['Name'])):
            debater_id = int(self.df.loc[x]['Debater ID'])
            name_excel = self.df.loc[x]['Name']
            name_system = match_id_to_name(debater_id)

            if name_excel != name_system:
                print(name_excel + ' : ' + str(debater_id))
                return False

        print('Finished!')
        return True


def create_new_user(name: str) -> int:
    """If a given user does not exist, create the new user. return the new user ID"""
    new_debater = AddDebater(name)
    return new_debater.add_debater_id()


file = ExcelReader()
file.add_tournament_data()
