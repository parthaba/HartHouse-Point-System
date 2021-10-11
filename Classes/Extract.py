import json
from typing import List, Tuple


def add_entry(semester_logged: str, id: int, id_debater: int, name: str, service: bool, judging: bool,
              tournament: str, semester: str, points: int) -> None:
    """Add a tournament data entry to JSON file.
    Representation Invariants:
    - semesters MUST be recorded as "Semester Year" ie. Fall 2021 or Winter 2053
    """

    with open(semester_logged) as json_file:
        tournament_records = json.load(json_file)
        tournament_records['entry'].append(
            {
                'id': id,
                'id_debater': id_debater,
                'name': name,
                'service': service,
                'judging': judging,
                'tournament': tournament,
                'semester': semester,
                'points': points
            })

    print(json.dumps(tournament_records, indent=4))


def delete_entry(id: int, id_debater: int, name: str, service: bool, judging: bool, tournament: str, semester: str,
                 points: int):
    """Delete a tournament data entry from JSON file."""

    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)

        entry = find_entry_id(id)

        tournament_records['entry'].remove(
            {
                'id': entry['id'],
                'id_debater': entry['id_debater'],
                'name': entry['name'],
                'service': entry['service'],
                'judging': entry['judging'],
                'tournament': entry['tournament'],
                'semester': entry['semester'],
                'points': entry['points']
            })

    print(json.dumps(tournament_records, indent=4))


def find_entry_id(id: int) -> dict:
    """Find a data entry in the master file using its id."""
    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)
        entry_list = tournament_records['entry']

        for entry in entry_list:
            if id == entry['id']:
                return entry

        raise ValueError


def find_entry_debater_id(debater_id: int) -> List[dict]:
    """Find all entries in the master file with a specific debater id."""
    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)
        entry_list = tournament_records['entry']
        return_list = []

        for entry in entry_list:
            if debater_id == entry['id_debater']:
                return_list.append(entry)

        return return_list


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


def get_top_five(semester: str, debater_id: int) -> int:
    """
    Return the total points from a debaters top 5 tournaments attended that semester
    Note this only includes at max 3 competitive tournaments.
    """
    tourn_counter = 0  # Keeps count of total tournaments up to 5
    comp_tourn = 0  # Keeps count of total competitive tournaments up to 3
    points = 0

    entry_list = find_entry_debater_id(debater_id)
    filtered_list = []

    # Creating the filtered list one tournament at a time
    for entry in entry_list:
        if (entry['semester'] == semester) and (entry['service'] is False):
            filtered_list.append(entry)

    # Organizing the filtered list
    # This will sort the list by points in descending order
    filtered_list.sort(key=lambda x: x.get('points'), reverse=True)

    for entry in filtered_list:

        # Check if the tournament was judging or competitive; add points accordingly
        if entry["judging"]:
            tourn_counter += 1
            points += entry['points']

        elif comp_tourn < 3:
            tourn_counter += 1
            comp_tourn += 1
            points += entry['points']

        # Can only have 5 tournaments max
        if tourn_counter == 5:
            break

    return points


def tournament_bid(teams: List[Tuple], limit: int) -> str:
    """Given a list of tuples with team debater IDs, return the teams that auto-qualify."""


def last_four_semester(debater_id: int) -> List[str]:
    """
    Return the alst 4 semesters a debater has debated in.
    """

    # TODO: Answer these questions
    # What about ongoing semesters?
    # What if they skip a year and come back?
    # If they don't want a semester included?

    entry_list = find_entry_debater_id(debater_id)
    highest_date = []

    # Populating the list of highest dates. The way it works is "Winter 2020" becomes 2020.5 and
    # "Fall 2030" becomes 2030. Ie. Winter semesters get an additional .5 added onto the year
    for entry in entry_list:
        if entry['date'][0] == 'W':
            year = int(entry['date'][7:11]) + 0.5
        else:
            year = int(entry['date'][5:9])
        highest_date.append(year)

    # Determine the highest semester this debater has debated in
    max_date = max(highest_date)

    # If this debater's last semester was Fall:
    if max_date % 1 == 0:
        max_date_str = "Fall " + str(int(max_date))
        one_sem_before = "Winter " + str(int(max_date - 1))
        two_sem_before = "Fall " + str(int(max_date - 1))
        three_sem_before = "Winter " + str(int(max_date - 2))

    # If this debater's last semester was Winter
    else:
        max_date_str = "Winter " + str(int(max_date))
        one_sem_before = "Fall " + str(int(max_date))
        two_sem_before = "Winter " + str(int(max_date - 1))
        three_sem_before = "Fall " + str(int(max_date - 1))

    # return a list of the last 4 semesters in string format
    return [max_date_str, one_sem_before, two_sem_before, three_sem_before]


def calculate_total_points(debater_id: int) -> int:
    """
    Calculate a debaters total relevant points
    """

    return (calculate_comp_points(debater_id)
            + calculate_service_points(debater_id))


def calculate_service_points(debater_id: int) -> int:
    """
    Calculate a debaters total service points.
    """
    entry_list = find_entry_debater_id(debater_id)
    four_semesters = last_four_semester(debater_id)

    total_service_points = 0

    filtered_entry_list = []

    for entry in entry_list:
        if entry['service']:
            filtered_entry_list.append(entry)

    for semester in four_semesters:
        service_points = 0
        for entry in filtered_entry_list:
            if semester == entry['date']:
                service_points += entry['points']

        total_service_points += min(30, service_points)



def calculate_comp_points(debater_id: int) -> int:

