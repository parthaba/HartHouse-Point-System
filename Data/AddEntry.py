from Classes.Extract import add_entry
from datetime import datetime


class AddEntry:
    """Add an entry into one of the semester files."""
    FALL_2019 = "Debaters/Fall 2019.txt"
    WINTER_2020 = "Debaters/Winter 2020.txt"
    FALL_2020 = "Debaters/Fall 2020.txt"
    WINTER_2021 = "Debaters/Winter 2021.txt.txt"
    SEMESTER_DICT = {"Fall 2019": FALL_2019,
                     "Winter 2020": WINTER_2021,
                     "Fall 2020": FALL_2020,
                     "Winter 2021.txt": WINTER_2021}

    entry_id: int
    debater_id: int
    debater_name: str
    semester_file: str
    semester: str

    def __init__(self):
        """Initialize an AddEntry object."""
        debater_id = int(input("Enter the debater ID: "))
        semester = input("Enter the semester (e.x Fall 2018): ")

        self.entry_id = self.create_unique_entry_id()
        self.debater_id = debater_id
        self.debater_name = self.match_id_to_name(debater_id)
        self.semester = semester
        self.semester_file = self.SEMESTER_DICT[semester]

    def match_id_to_name(self, debater_id: int) -> str:
        """Given a debater_id, return the matching name. If no such name exists, raise a ValueError."""
        # TODO: implement this method

    def add_debater_entry(self) -> None:
        """Add points to a debater."""

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
        """Adds service points to a member of the club."""
        points = int(input("Enter the amount of service points earned as an integer."))

        # For service points, the tournament attribute is left as an empty string.
        add_entry(self.semester_file,
                  self.entry_id,
                  self.debater_id,
                  self.debater_name,
                  service=True,
                  judging=False,
                  tournament='',
                  semester=self.semester,
                  points=points)

    def add_tournament_points(self) -> None:
        """Depending on whether the debater judged or competed, add the appropriate points."""

        tournament_name = input("Enter the tournament name: ")

        judging = input("Did this person judge? Enter <y> if yes, enter <n> if no.")
        if judging == 'y' or judging == "Y" or judging == '<y>':

            # Judging
            points = self.tournament_judging()

            add_entry(self.semester_file,
                      self.entry_id,
                      self.debater_id,
                      self.debater_name,
                      False,
                      True,
                      tournament_name,
                      self.semester,
                      points)


        elif judging == 'n' or judging == "N" or judging == '<n>':

            # Debating
            points = self.tournament_debating()

            add_entry(self.semester_file,
                      self.entry_id,
                      self.debater_id,
                      self.debater_name,
                      False,
                      False,
                      tournament_name,
                      self.semester,
                      points)
        else:
            raise ValueError

    def tournament_judging(self) -> int:
        """Calculate points earned from judging."""

    def tournament_debating(self) -> int:
        """Calculate points earned from debating."""

    def create_unique_entry_id(self) -> int:
        """Generate a valid (unique 6 digit long) ID for a new data entry."""

    def calculate_points(tier: int, team_place: int, speaker_place: int, size_teams: int) -> int:
        """Calculate the number of competitive points earned from a tournament."""
        if tier == 1:
            max_points_team = 50
            max_points_speaker = 40
        elif tier == 2:
            max_points_team = 30
            max_points_speaker = 24
        elif tier == 3:
            max_points_team = 20
            max_points_speaker = 16
        else:
            max_points_team = 10
            max_points_speaker = 8

        speaker_points = max_points_speaker - (max_points_speaker * (speaker_place - 1)) / size_teams
        if speaker_points < 0:
            speaker_points = 0

        team_points = max_points_team - (max_points_team * 2 * (team_place - 1)) / size_teams
        if team_points < 0:
            team_points = 0

        print("Speaker points:" + str(speaker_points))
        print("Team points:" + str(team_points))
        return speaker_points + team_points


