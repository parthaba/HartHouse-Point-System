import json
from typing import List


class Semester:
    """
    Represents all the tournaments debated at, tournaments judged at, and service points earned by ALL Hart House
    members in a single semester.

    Instance attributes:
    - entry_list: A list of every tournament that all debaters have attended in a semester
    - semester: The semester of this semester class
    - date: The date of that semester

    Methods:
    - top_five_tournaments: Return the top 5 tournaments that a debater has attended
        Note that this can only include at max 3 debating tournaments and at max 5 judging tournaments
    - service_tournaments: Return all service related events that an individual has attended
    """

    def __init__(self, semester: str, semester_file: str, entry_list: List[dict]):
        self.semester = semester
        self.semester_file = semester_file
        with open(semester_file) as json_file:
            semester_records = json.load(json_file)
            entry_list = semester_records['entry']

        self.entry_list = entry_list

    def find_entry_debater_id(self, debater_id: int) -> List[dict]:
        """Find all entries in the master file with a specific debater id."""
        return_list = []

        for entry in self.entry_list:
            if debater_id == entry['id_debater']:
                return_list.append(entry)

        return return_list

    def calculate_service_points(self, debater_id: int) -> int:
        """
        Calculate a debaters total service points.
        """
        entry_list = self.find_entry_debater_id(debater_id)
        four_semesters = self.last_four_semester(debater_id)
        three_semesters = four_semesters[0:3]

        total_service_points = 0

        filtered_entry_list = []

        for entry in entry_list:
            if entry['service']:
                filtered_entry_list.append(entry)

        for semester in three_semesters:
            service_points = 0
            for entry in filtered_entry_list:
                if semester == entry['date']:
                    service_points += entry['points']

            total_service_points += min(30, service_points)

    def calculate_comp_points(self, debater_id: int) -> int:
        pass

    def calculate_total_points(self, debater_id: int) -> int:
        """
        Calculate a debaters total relevant points
        """

        return (self.calculate_comp_points(debater_id)
                + self.calculate_service_points(debater_id))
