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
    """ Return the total points from a debaters top 5 tournaments attended that semester
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


def top_four_semester():
    """"""
