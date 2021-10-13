import json
from typing import List, Tuple


def add_entry(semester_logged: str, entry_id: int, id_debater: int, name: str, service: bool, service_position: bool, judging: bool,
              tournament: str, semester: str, points: int) -> None:
    """Add a tournament data entry to JSON file.
    Representation Invariants:
    - semesters MUST be recorded as "Semester Year" ie. Fall 2021 or Winter 2053
    """
    filename = semester_logged
    entry = {'entry_id': entry_id,
             'id_debater': id_debater,
             'name': name,
             'service': service,
             'service_position': service_position,
             'judging': judging,
             'tournament': tournament,
             'semester': semester,
             'points': points
             }

    with open(filename, 'r') as file:
        data = json.load(file)['entry']

    data.append(entry)

    new_data = {'entry': data}

    with open(filename, 'w') as file:
        json.dump(new_data, file, indent=4)

    print("Successfully added!")


def delete_entry(id: int, id_debater: int, name: str, service: bool, service_position: bool, judging: bool, tournament: str, semester: str,
                 points: int):
    """Delete a tournament data entry from JSON file."""

    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)

        entry = find_entry_id(id)

        tournament_records['entry'].remove(
            {
                'id': entry[id],
                'id_debater': entry[id_debater],
                'name': entry[name],
                'service': entry[service],
                'service_position': entry[service_position],
                'judging': entry[judging],
                'tournament': entry[tournament],
                'semester': entry[semester],
                'points': entry[points]
            })

    print(json.dumps(tournament_records, indent=4))


def find_entry_id(debater_id: int) -> dict:
    """Find a data entry in the master file using its id."""
    with open('tournament_records.txt') as json_file:
        tournament_records = json.load(json_file)
        entry_list = tournament_records['entry']

        for entry in entry_list:
            if debater_id == entry['id']:
                return entry

        raise ValueError


def tournament_bid(teams: List[Tuple], limit: int) -> str:
    """Given a list of tuples with team debater IDs, return the teams that auto-qualify."""






