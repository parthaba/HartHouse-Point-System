import json
from typing import List
import os


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

    def __init__(self, semester: str, semester_file: str):
        self.semester = semester
        self.semester_file = semester_file

        if semester[0] == 'W':
            self.num_represent = int(semester[7:11]) + 0.5
        else:
            self.num_represent = int(semester[5:9])

        abs_path = os.getcwd()
        sem_directory = abs_path + '/../Data/Semesters/'
        semester_file = sem_directory + semester_file
        with open(semester_file) as json_file:
            semester_records = json.load(json_file)
            entry_list = semester_records['entry']

        self.entry_list = entry_list

    def __str__(self):
        return self.semester

    def find_entry_debater_id(self, debater_id: int) -> List[dict]:
        """Find all entries in the master file with a specific debater id."""
        return_list = []

        for entry in self.entry_list:
            if debater_id == entry['id_debater']:
                return_list.append(entry)

        return return_list

    def __lt__(self, other) -> bool:
        if isinstance(other, int) or isinstance(other, float):
            if self.num_represent < other:
                return True

        elif self.num_represent < other.num_represent:
            return True
        return False

    def __gt__(self, other) -> bool:
        if isinstance(other, int) or isinstance(other, float):
            if self.num_represent > other:
                return True

        elif self.num_represent > other.num_represent:
            return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, int) or isinstance(other, float):
            if self.num_represent == other:
                return True

        elif self.num_represent == other.num_represent:
            return True
        return False
