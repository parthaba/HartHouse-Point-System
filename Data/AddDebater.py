import random
import csv


class AddDebater:
    """Add a new debater and ID pairing to the id_list."""

    # name of the csv file
    FILENAME = "Debaters/id_list.csv"

    def __init__(self):
        """Create new AddDebater object."""

    def create_valid_id(self) -> int:
        """Create a valid (unique 6 digit long) ID for a new debater"""

        id_list = list(range(0, 1000000))

        with open(self.FILENAME, 'r') as csvfile:
            # creating a csv writer object
            csv_reader = csv.reader(csvfile)

            # writing the fields
            fields = next(csv_reader)

            # accumulator for used IDs
            used_id_list = []
            row_number = 0
            for row in csv_reader:

                # filters out empty rows
                row_number += 1
                if row_number % 2 == 0:
                    # keeps track of IDs that have already been used
                    used_id_list.append(row[1])

        valid_id_list = [user_id for user_id in id_list
                         if user_id not in used_id_list]

        return random.choice(valid_id_list)

    def add_debater_id(self) -> None:
        """Add a new debater to id_list.csv. The debater will have a unique, randomized 6 digit
        number as their ID."""

        # debater name and generated id
        debater_name = input("Enter the name of the debater you want to add: ")
        debater_id = self.create_valid_id()

        with open(self.FILENAME, 'a') as csvfile:
            # creating a csv writer object
            csv_writer = csv.writer(csvfile)

            # writing the fields
            csv_writer.writerow([debater_name, debater_id])

        print(debater_name + ": " + str(debater_id) + " has been successfully added!")


new_debater = AddDebater()
new_debater.add_debater_id()
