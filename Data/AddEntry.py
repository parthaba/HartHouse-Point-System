from Classes.Extract import add_entry
from datetime import datetime


class AddEntry:
    """Add an entry into one of the semester files."""
    FALL_2020 = "Fall 2020.txt"
    WINTER_2021 = "Winter 2021.txt"

    def add_debater_entry(self) -> None:
        """"""
        entry_id = self.create_unique_entry_id()

        debater_id = debater_id = int(input("Enter debater id: "))

        # TODO: use csv reader to match debater_id to debater_name
        debater_name = ...


        continue_adding = True
        while continue_adding == True:

            # For adding service points
            service = input("Are these service points? Enter <y> if yes, enter <n> if no.")
            if service == 'y' or service == "Y" or service == '<y>':
                self.add_service_points()
            elif service == 'n' or service == "N" or service == '<n>':
                service = False
            else:
                raise ValueError

            # For adding tournament points
            self.add_tournament_points()

            # Give option to add another entry
            continue_add = input("Would you like to add another data entry for this debater? "
                                 "Enter <y> if yes, enter <n> if no.")
            if continue_add == 'y' or continue_add == "Y" or continue_add == '<y>':
                continue_adding = True
            elif service == 'n' or service == "N" or service == '<n>':
                continue_adding = False
            else:
                raise ValueError

    def add_service_points(self) -> None:
        """"""

    def add_tournament_points(self) -> None:
        """Depending on whether the debater judged or competed, add the appropriate points."""

    def tournament_judging(self) -> None:
        """Calculate points earned from judging."""

    def tournament_debating(self) -> None:
        """Calculate points earned from debating."""

    def create_unique_entry_id(self) -> int:
        """Generate a valid (unique 6 digit long) ID for a new data entry."""

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
