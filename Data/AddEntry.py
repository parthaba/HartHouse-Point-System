from Classes.Extract import add_entry
import random
import csv


class AddEntry:
    """Add an entry into one of the semester files."""

    FALL_2018 = "Semesters/Fall 2018.json"
    FALL_2019 = "Semesters/Fall 2019.json"
    FALL_2020 = "Semesters/Fall 2020.json"
    FALL_2021 = "Semesters/Fall 2021.json"
    WINTER_2018 = "Semesters/Winter 2018.json"
    WINTER_2019 = "Semesters/Winter 2019.json"
    WINTER_2020 = "Semesters/Winter 2020.json"
    WINTER_2021 = "Semesters/Winter 2021.json."

    SEMESTER_DICT = {"Fall 2019": FALL_2019,
                     "Winter 2020": WINTER_2021,
                     "Fall 2020": FALL_2020,
                     "Winter 2021": WINTER_2021,
                     "Fall 2017": FALL_2017,
                     "Fall 2018": FALL_2018,
                     "Winter 2019": WINTER_2019,
                     "Winter 2018": WINTER_2018}

    SEMESTER_LIST = ['Fall 2017', 'Fall 2018', 'Fall 2019', 'Fall 2020',
                     'Winter 2018', 'Winter 2019', 'Winter 2020', 'Winter 2021']

    entry_id: int
    debater_id: int
    debater_name: str
    semester_file: str
    semester: str

    def __init__(self, debater_id: int, semester: str):
        """Initialize an AddEntry object."""

        self.entry_id = create_unique_entry_id()
        self.debater_id = debater_id
        self.debater_name = match_id_to_name(debater_id)

        if semester in self.SEMESTER_LIST:
            self.semester_file = self.SEMESTER_DICT[semester]
            self.semester = semester
        else:
            raise ValueError

    def record_entry_id(self) -> None:
        """Record the unique entry_id used."""

        with open("data_entry_ids.csv", 'a') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([self.entry_id])

    def add_service_points(self, points: int, position: bool) -> None:
        """Adds service points to a member of the club."""

        add_entry(self.semester_file,  # Which semester file
                  self.entry_id,  # Unique entry ID
                  self.debater_id,  # Debater ID
                  self.debater_name,  # Debater name
                  True,  # Whether these are service points
                  position,  # If service points, whether from specific position or outreach
                  False,  # Judging
                  '',  # Name of tournament (if service, empty string)
                  self.semester,  # The semester that these points were earned
                  points)  # The number of points earned

        self.record_entry_id()

    def tournament_judging(self, tier: int, tournament_name: str, break_as_judge: bool) -> None:
        """Calculate points earned from judging."""

        points = calculate_points_judging(tier, break_as_judge)

        add_entry(self.semester_file,  # Which semester file
                  self.entry_id,  # Unique entry ID
                  self.debater_id,  # Debater ID
                  self.debater_name,  # Debater name
                  False,  # Whether these are service points
                  False,  # If service points, whether from specific position or outreach
                  True,  # Judging
                  tournament_name,  # Name of tournament (if service, empty string)
                  self.semester,  # The semester that these points were earned
                  points)  # The number of points earned

        self.record_entry_id()

    def tournament_debating(self, tier: int, tournament_name: str, tournament_size: int,
                            team_place: int, speaker_place: int) -> None:
        """Calculate points earned from debating."""

        points = calculate_points_debating(tier, tournament_size, team_place, speaker_place)

        add_entry(self.semester_file,  # Which semester file
                  self.entry_id,  # Unique entry ID
                  self.debater_id,  # Debater ID
                  self.debater_name,  # Debater name
                  False,  # Whether these are service points
                  False,  # If service points, whether from specific position or outreach
                  False,  # Judging
                  tournament_name,  # Name of tournament (if service, empty string)
                  self.semester,  # The semester that these points were earned
                  points)  # The number of points earned

        self.record_entry_id()


def create_unique_entry_id() -> int:
    """Generate a valid (unique 6 digit long) ID for a new data entry."""
    id_list = list(range(100000, 1000000))
    used_id_list = []
    with open("data_entry_ids.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        row_count = 1

        for row in csv_reader:

            if row_count % 2 == 1:
                used_id_list.append(row[0])

            row_count += 1

    valid_id_list = [user_id for user_id in id_list
                     if str(user_id) not in used_id_list]

    return random.choice(valid_id_list)


def match_id_to_name(debater_id: int) -> str:
    """Given a debater_id, return the matching name. If no such name exists, raise a ValueError."""
    with open("Debaters/id_list.csv", 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        row_number = 1
        for row in csv_reader:

            # filters out empty rows
            if row_number % 2 == 1:

                # Return the name of the debater with the given debater ID
                if row[1] == str(debater_id):
                    return row[0]

            row_number += 1

        print(debater_id)
        raise Exception("Did not find a debater with this ID.")


def calculate_points_debating(tier: int, size_teams: int, team_place: int, speaker_place: int) -> int:
    """Calculate the number of competitive points earned from debating at a tournament."""
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

    # print("Speaker points:" + str(speaker_points))
    # print("Team points:" + str(team_points))
    return speaker_points + team_points


def calculate_points_judging(tier: int, break_as_judge: bool) -> int:
    """Calculate the number of competitive points earned from judging at a tournament."""

    if tier == 1:
        if break_as_judge:
            return 45
        else:
            return 15

    elif tier == 2:
        if break_as_judge:
            return 27
        else:
            return 9

    elif tier == 3:
        if break_as_judge:
            return 18
        else:
            return 6

    else:
        if break_as_judge:
            return 9
        else:
            return 3

