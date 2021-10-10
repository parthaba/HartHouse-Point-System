from Classes.Extract import add_entry
from datetime import datetime


class AddEntry:
    """Add an entry into one of the semester files."""
    FALL_2020 = "Fall 2020.txt"
    WINTER_2021 = "Winter 2021.txt"

    def add_debater_points(self) -> None:
        """"""

    if __name__ == "__main__":
        id = int(input("Enter entry id: "))

        debater_id = int(input("Enter debater id: "))

        name = input("Enter debater name: ")

        service = input("Are these service points? Enter <y> if yes, enter <n> if no.")
        if service == 'y' or service == "Y" or service == '<y>':
            service = True
        elif service == 'n' or service == "N" or service == '<n>':
            service = False
        else:
            raise ValueError

        judging = input("Did this person judge? Enter <y> if yes, enter <n> if no.")
        if judging == 'y' or service == "Y" or service == '<y>':
            judging = True
        elif judging == 'n' or service == "N" or service == '<n>':
            judging = False
        else:
            raise ValueError

        tournament = input("Enter the name of the tournament: ")

        semester = input("Enter the semester that this entry is being logged for: ")

        points = 10

        add_entry(FALL_2020,
                  id,
                  debater_id,
                  name,
                  service,
                  judging,
                  tournament,
                  semester,
                  points)
