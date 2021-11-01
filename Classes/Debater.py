from typing import List
import os
import csv
from Classes.Semester import Semester


class Debater:
    """
    Represents a debater in the Hart House debate club
    
    Instance Attributes:
    - debater_id: the id of the debater
    - name: the name of the debater
    - working_points: Total amount of RELEVANT points (over the past 4 semesters/including any multipliers/
                    service points included/only top 5 tournaments etc.)
    - tour_attended: A dictionary of all tournaments attended along with the points accumulated at each tournament
    
    Methods:
    - semester_points: Returns the number of points earned for a specific semester
    - tournament_points: Returns the points gained from ALL years attending a specific tournament.

    Representation Invariants:
    - debater_id must be a positive integer
    - working_points must be a positive integer
    """

    debater_id: int
    working_points: float
    tour_attended: dict
    name: str
    _current_semester: Semester

    def __init__(self, debater_id: int) -> None:
        """ Initialize a debater """

        self.debater_id = debater_id

        self.tour_attended = {}

        # Allocating name
        with open('../Data/Debaters/id_list.csv') as name_file:
            csv_reader = csv.reader(name_file, delimiter=',')
            id_reader = []
            for row in csv_reader:
                if row:
                    if row[1][1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        id_reader.append(row)
            for row in id_reader:
                if int(row[1]) == debater_id:
                    self.name = str(row[0])
                    break

        # Determining the current semester and creating tournament list
        # Finding the Semesters directory
        abs_path = os.getcwd()
        sem_directory = abs_path + '/../Data/Semesters'

        # populating a list of all semester files
        semester_file_list = os.listdir(sem_directory)

        # Cycling through each file and turning them into Semester objects.
        sem_list = []
        for file in semester_file_list:
            sem_str = file.strip('.json')
            sem = Semester(sem_str, file)
            sem_list.append(sem)

        self._current_semester = max(sem_list)

        # Populating event/tournament list
        service_num = 1
        for sem in sem_list:
            tourn_list = sem.find_entry_debater_id(self.debater_id)
            for tourn in tourn_list:
                if tourn["service"] == True:
                    self.tour_attended[tourn["semester"] + ": Service " + str(service_num)] = tourn["points"]
                    service_num += 1
                else:
                    self.tour_attended[tourn["semester"] + ": " + tourn["tournament"]] = tourn["points"]

        self.working_points = self.calculate_total_points()

    def __str__(self) -> str:
        """
        String representation of debater instance
        Will return Name, debater id, and relevant tournament list. ie.

        Name: Ameen Parthab
        id: 1
        Tournaments attended
        WUDC Fall 2019 > 89.123120938102938
        HWS RR Winter 2020 > 88.123123123123123

        """

        return (
                'Name: ' + self.name + '\n' +
                'ID: ' + str(self.debater_id) + '\n' +
                'Total Points: '+ str(self.working_points) + '\n' +
                '--- Tournaments/Events Attended --- \n' +
                self.all_relevant_tourn_str().strip('\n')
        )

    def set_working_points(self, points: float):
        """Setter method for self.working_points."""
        self.working_points = points

    def reset_debater(self, name: str, points: float):
        """Set name and point values for a Debater object."""
        self.name = name
        self.working_points = points

    def return_tournaments(self) -> str:
        """ Return all tournaments attended """
        return_str = ''

        for tour in self.tour_attended:
            return_str = return_str + tour + ' > ' + str(self.tour_attended[tour]) + '\n'

        return return_str

    def last_four_semesters(self) -> List[Semester]:
        """
        Return the last 4 semesters a debater has debated in.
        """

        # Finding the Semesters directory
        abs_path = os.getcwd()
        sem_directory = abs_path + '/../Data/Semesters'

        # populating a list of all semester files
        semester_file_list = os.listdir(sem_directory)

        # Cycling through each file and turning them into Semester objects. Also checking whether a debater has debated
        # in these semesters or not
        sem_list = []
        for file in semester_file_list:

            sem_str = file.strip('.json')
            sem = Semester(sem_str, file)

            debater_list = sem.find_entry_debater_id(self.debater_id)

            # If the debater has debated in this semester, add them to the count
            # NOTE that this includes semesters that people have serviced in but NOT debated in. I'm not sure if this is
            # illegal but honestly that's not my issue :)
            if debater_list:
                sem_list.append(sem)

        # If the debater has not debated in any semesters, return an empty list.
        if len(sem_list) == 0:
            return []

        # Determine the highest semester this debater has debated in
        max_sem = max(sem_list)
        max_date = max_sem.num_represent

        # If this debater's last semester was Fall:
        if max_date % 1 == 0:
            one_sem_before = Semester("Winter " + str(int(max_date)), "Winter " + str(int(max_date)) + ".json")
            two_sem_before = Semester("Fall " + str(int(max_date - 1)), "Fall " + str(int(max_date - 1)) + ".json")
            three_sem_before = Semester("Winter " + str(int(max_date - 1)),
                                        "Winter " + str(int(max_date - 1)) + ".json")

        # If this debater's last semester was Winter
        else:
            one_sem_before = Semester("Fall " + str(int(max_date - 1)), "Fall " + str(int(max_date - 1)) + ".json")
            two_sem_before = Semester("Winter " + str(int(max_date - 1)), "Winter " + str(int(max_date - 1)) + ".json")
            three_sem_before = Semester("Fall " + str(int(max_date - 2)), "Fall " + str(int(max_date - 2)) + ".json")

        # return a list of the last 4 semesters a debater has debated in
        return [max_sem, one_sem_before, two_sem_before, three_sem_before]

    def last_four_semester_minus_current(self) -> List[Semester]:
        """
        Return the last 4 semesters a debater has debated in.
        Note that this doesn't count the CURRENT SEMESTER
        """

        # Finding the Semesters directory
        abs_path = os.getcwd()
        sem_directory = abs_path + '/../Data/Semesters'

        # populating a list of all semester files
        semester_file_list = os.listdir(sem_directory)

        # Filtering out the current semester
        sem_missing_current = list(filter(self._current_semester.semester_file.__ne__, semester_file_list))

        # Cycling through each file and turning them into Semester objects. Also checking whether a debater has debated
        # in these semesters or not
        sem_list = []
        for file in sem_missing_current:

            sem_str = file.strip('.json')
            sem = Semester(sem_str, file)

            debater_list = sem.find_entry_debater_id(self.debater_id)

            # If the debater has debated in this semester, add them to the count
            # NOTE that this includes semesters that people have serviced in but NOT debated in. I'm not sure if this is
            # illegal but honestly that's not my issue :)
            if debater_list:
                sem_list.append(sem)

        if not sem_list:
            return []

        # Determine the highest semester this debater has debated in
        max_sem = max(sem_list)
        max_date = max_sem.num_represent

        # If this debater's last semester was Fall:
        if max_date % 1 == 0:
            one_sem_before = Semester("Winter " + str(int(max_date)), "Winter " + str(int(max_date)) + ".json")
            two_sem_before = Semester("Fall " + str(int(max_date - 1)), "Fall " + str(int(max_date - 1)) + ".json")
            three_sem_before = Semester("Winter " + str(int(max_date - 1)),
                                        "Winter " + str(int(max_date - 1)) + ".json")

        # If this debater's last semester was Winter
        else:
            one_sem_before = Semester("Fall " + str(int(max_date - 1)), "Fall " + str(int(max_date - 1)) + ".json")
            two_sem_before = Semester("Winter " + str(int(max_date - 1)), "Winter " + str(int(max_date - 1)) + ".json")
            three_sem_before = Semester("Fall " + str(int(max_date - 2)), "Fall " + str(int(max_date - 2)) + ".json")

        # return a list of the last 4 semesters a debater has debated in
        return [max_sem, one_sem_before, two_sem_before, three_sem_before]

    def get_top_five_sem(self, sem: Semester) -> int:
        """
        Return the total points from a debaters top 5 tournaments attended that semester
        Note this only includes at max 3 competitive tournaments.
        """
        tourn_counter = 0  # Keeps count of total tournaments up to 5
        comp_tourn = 0  # Keeps count of total competitive tournaments up to 3
        points = 0

        entry_list = sem.find_entry_debater_id(self.debater_id)
        filtered_list = []

        # Creating the filtered list one tournament at a time
        for entry in entry_list:
            if (entry['semester'] == sem.semester) and (entry['service'] is False):
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

    def get_top_five_sem_returnstr(self, sem: Semester) -> str:
        """
        Return the total points from a debaters top 5 tournaments attended that semester
        Note this only includes at max 3 competitive tournaments.
        """
        tourn_counter = 0  # Keeps count of total tournaments up to 5
        comp_tourn = 0  # Keeps count of total competitive tournaments up to 3
        return_str = ''

        entry_list = sem.find_entry_debater_id(self.debater_id)
        filtered_list = []

        # Creating the filtered list one tournament at a time
        for entry in entry_list:
            if (entry['semester'] == sem.semester) and (entry['service'] is False):
                filtered_list.append(entry)

        # Organizing the filtered list
        # This will sort the list by points in descending order
        filtered_list.sort(key=lambda x: x.get('points'), reverse=True)

        for entry in filtered_list:

            # Check if the tournament was judging or competitive; add points accordingly
            if entry["judging"]:
                tourn_counter += 1
                return_str = return_str + entry["semester"] + ": " + entry["tournament"] + ' (Judging) > ' + str(entry["points"]) + '\n'

            elif comp_tourn < 3:
                tourn_counter += 1
                comp_tourn += 1
                return_str = return_str + entry["semester"] + ": " + entry["tournament"] + ' > ' + str(entry["points"]) + '\n'

            # Can only have 5 tournaments max
            if tourn_counter == 5:
                break

        return return_str

    def all_relevant_tourn_str(self) -> str:
        return_str = ''
        curr_num = self._current_semester.num_represent
        four_sem = self.last_four_semester_minus_current()

        if len(four_sem) == 0:
            return_str = ""

        elif (curr_num - 0.5 == four_sem[0] or
                curr_num - 1 == four_sem[0] or
                curr_num - 1.5 == four_sem[0]):

            for sem in four_sem:
                return_str += self.get_top_five_sem_returnstr(sem)

        else:
            for sem in four_sem:
                if curr_num - 3 <= sem.num_represent:
                    return_str += self.get_top_five_sem_returnstr(sem)

        return return_str

    def return_semester_breakdown(self, sem: str):
        """Return the relevant tournaments and their corresponding point totals from a given semester."""
        # TODO: Implement this function

    def calculate_service_points_sem(self, sem: Semester, last_in_list: bool) -> int:
        """
        Calculate a debaters service points in one semester
        """

        entry_list = sem.find_entry_debater_id(self.debater_id)

        filtered_entry_list = []

        # Creating the filtered list one event at a time
        for entry in entry_list:
            if entry['service']:
                filtered_entry_list.append(entry)

        service_points = 0

        if not last_in_list:
            for entry in filtered_entry_list:
                service_points += entry['points']

        else:
            for entry in filtered_entry_list:
                if entry['service_position']:
                    service_points += entry['points']
                else:
                    service_points += .75 * entry['points']

        return service_points

    def calculate_service_points(self):
        curr_num = self._current_semester.num_represent
        three_sem = self.last_four_semesters()

        service_points = 0
        # If the debater has not done any service, return 0.
        if len(three_sem) == 0:
            return service_points

        if curr_num == three_sem[0]:
            service_points += self.calculate_service_points_sem(three_sem[0], False)
            service_points += self.calculate_service_points_sem(three_sem[1], False)
            service_points += self.calculate_service_points_sem(three_sem[2], True)

        elif curr_num - 0.5 == three_sem[0] or curr_num - 1 == three_sem[0]:
            service_points += self.calculate_service_points_sem(three_sem[0], False)
            service_points += self.calculate_service_points_sem(three_sem[1], True)

        else:
            for sem in three_sem:
                if curr_num - 2 <= sem.num_represent:
                    service_points += self.calculate_service_points_sem(sem, True)

        return min(service_points, 30)

    def calculate_comp_points(self) -> int:
        comp_points = 0
        curr_num = self._current_semester.num_represent
        four_sem = self.last_four_semester_minus_current()

        if len(four_sem) == 0:
            return 0

        if (curr_num - 0.5 == four_sem[0] or
                curr_num - 1 == four_sem[0] or
                curr_num - 1.5 == four_sem[0]):

            for sem in four_sem:
                comp_points += self.get_top_five_sem(sem)
        else:
            for sem in four_sem:
                if curr_num - 3 <= sem.num_represent:
                    comp_points += self.get_top_five_sem(sem)
        return comp_points

    def multiplier(self) -> float:
        four_sem = self.last_four_semester_minus_current()
        semesters_debated = 0
        for sem in four_sem:
            if sem.find_entry_debater_id(self.debater_id):
                semesters_debated += 1

        if semesters_debated == 0:
            return 0
        elif semesters_debated == 1:
            return 4
        elif semesters_debated == 2:
            return 2
        elif semesters_debated == 3:
            return 4 / 3

    def calculate_total_points(self) -> int:
        """
        Calculate a debaters total relevant points
        """

        return int((self.multiplier() * self.calculate_comp_points())
                   + self.calculate_service_points())


