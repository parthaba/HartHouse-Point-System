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
                     "Winter 2020": WINTER_2020,
                     "Fall 2020": FALL_2020,
                     "Winter 2021": WINTER_2021,
                     "Fall 2021": FALL_2021}

    YES = ['y', 'Y', '<y>', 'yes', 'YES', 'Yes', 'yEs', 'yeS', 'YEs', 'yES', 'YeS']
    NO = ['n', 'N', '<n>', 'no', 'NO', 'No', 'nO']

    entry_id: int
    debater_id: int
    debater_name: str
    semester_file: str
    semester: str

    def __init__(self):
        """Initialize an AddEntry object."""
        debater_id = int(input("Enter the debater ID: "))

        self.debater_id = debater_id
        self.debater_name = match_id_to_name(debater_id)
        print("Debater: " + self.debater_name)

        continue_inputting = True
        while continue_inputting:
            self.add_entry()

            answer = input("Would you like to add another entry for this member?")
            if answer in self.NO:
                continue_inputting = False
            elif answer in self.YES:
                continue_inputting = True
            else:
                raise ValueError

    def add_entry(self) -> None:
        """Add points to a debater."""

        self.entry_id = create_unique_entry_id()

        semester = input("Enter the semester (e.x Fall 2018): ")
        self.semester = semester
        self.semester_file = self.SEMESTER_DICT[semester]

        service = input("Are these service points? Enter <y> if yes, enter <n> if no.")
        if service == 'y' or service == "Y" or service == '<y>':
            # Adding service points
            self.add_service_points()

        elif service == 'n' or service == "N" or service == '<n>':
            # Adding tournament points
            self.add_tournament_points()
        else:
            raise ValueError

        # Recording the ID used
        with open("data_entry_ids.csv", 'a') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([self.entry_id])

            # # Give option to add another entry
            # continue_add = input("Would you like to add another data entry for this debater? "
            #                      "Enter <y> if yes, enter <n> if no.")
            # if continue_add in self.YES:
            #     continue_adding = True
            # elif service == self.NO:
            #     continue_adding = False
            # else:
            #     raise ValueError

    def add_service_points(self) -> None:
        """Adds service points to a member of the club."""
        points = int(input("Enter the amount of service points earned as an integer."))
        position = input("Were these points earned from a special position? Enter <y> if yes, enter <n> if no.")
        if position in self.YES:
            position = True
        elif position in self.NO:
            position = False
        else:
            raise ValueError

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

    def add_tournament_points(self) -> None:
        """Depending on whether the debater judged or competed, add the appropriate points."""

        tournament_name = input("Enter the tournament name: ")
        tier = int(input("Enter the tier of the tournament: "))

        judging = input("Did this person judge? Enter <y> if yes, enter <n> if no.")
        if judging in self.YES:

            # Judging
            self.tournament_judging(tier, tournament_name)

        elif judging in self.NO:

            # Debating
            self.tournament_debating(tier, tournament_name)

        else:
            raise ValueError

    def tournament_judging(self, tier: int, tournament_name: str) -> None:
        """Calculate points earned from judging."""

        break_as_judge = input("Did this person break as a judge? Enter <y> if yes, <n> if no.")
        if break_as_judge in self.YES:
            break_as_judge = True
        elif break_as_judge in self.NO:
            break_as_judge = False
        else:
            raise ValueError

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

    def tournament_debating(self, tier: int, tournament_name: str) -> None:
        """Calculate points earned from debating."""
        tournament_size = int(input("Enter the number of teams at the tournament: "))
        team_place = int(input("Enter where this team ranked on the tab: "))
        speaker_place = int(input("Enter where this speaker ranked on the tab: "))

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


# Run the file
new_debater = AddEntry()
