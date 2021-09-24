import json
from typing import List, Tuple


def add_entry(id: int, id_debater: int, name: str, tournament: str, semester: str, points: int) -> str:
    """Add a tournament data entry to JSON file.
    >>> add_entry('Gautier', 'HHIV', 'Fall 2020')
    """

    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)
        tournament_records['entry'].append(
            {
                'id': id,
                'id_debater': id_debater,
                'name': name,
                'tournament': tournament,
                'semester': semester,
                'points': points
            })

    print(json.dumps(tournament_records, indent=4))

    update_debater_data(id_debater, name)


def delete_entry(id: int, id_debater: int, name: str, tournament: str, semester: str, points: int):
    """Delete a tournament data entry from JSON file."""

    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)

        entry = find_entry_id(id)

        tournament_records['entry'].remove(
            {
                'id': entry['id'],
                'id_debater': entry['id_debater'],
                'name': entry['name'],
                'tournament': entry['tournament'],
                'semester': entry['semester'],
                'points': entry['points']
            })

    print(json.dumps(tournament_records, indent=4))

    update_debater_data(id_debater, name)


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

        if not return_list:
            raise ValueError

        return return_list


def update_debater_data(id_debater: int, name: str) -> None:
    """Update the data of a debater with a recent tournament entry."""


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

    print("Speaker points:" + speaker_points)
    print("Team points:" + team_points)
    return speaker_points + team_points


def get_top_five():
    """"""


def get_top_three_debate(tournaments: list):
    """Get the top three highest point earning tournaments a debater spoke at."""


def find_debater(id_debater: int, name: str) -> json:
    """Input the name and id of a debater and output their information."""


def tournament_bid(teams: List[Tuple], limit: int) -> str:
    """Given a list of tuples with team debater IDs, return the teams that auto-qualify."""
