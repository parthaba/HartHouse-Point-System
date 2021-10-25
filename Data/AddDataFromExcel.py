import pandas as pd
from Data.AddEntry import AddEntry
from Data.AddEntry import match_id_to_name


class ExcelReader:
    """Reads rows from an excel sheet and uploads them to the respective JSON file."""

    df = pd.read_excel(r'C:\Users\james\OneDrive\Desktop\Points Coordinator\Winter 2021.xlsx',
                       sheet_name='Points Tracking')

    def __init__(self):
        """Initialize the ExcelReader."""

    def add_tournament_data(self):
        """Takes in data from excel spreadsheet for debate tournament results and adds them as competitive points."""

        for x in range(len(self.df['Name'])):
            debater_id = int(self.df.loc[x]['Debater ID'])
            semester = "Winter 2021"
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

    def check_name_to_id(self) -> None:
        """Check if the name and ID match. If not, print the occurrence."""
        for x in range(len(self.df['Name'])):
            debater_id = int(self.df.loc[x]['Debater ID'])
            name_excel = self.df.loc[x]['Name']
            name_system = match_id_to_name(debater_id)

            if name_excel != name_system:
                print(name_excel + ' : ' + str(debater_id))

        print('Finished!')


file = ExcelReader()
file.add_tournament_data()
