from typing import List

from Semester import Semester


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
    working_points: int
    tour_attended: dict
    name: str

    def __init__(self, debater_id: int) -> None:
        """ Initialize a debater """

        # TODO: Create a file that matches debater id to debater name. use this in the constructor
        self.name = ""
        self.debater_id = debater_id
        self.working_points = 0
        self.tour_attended = {}

        # Creating a list of all tournaments debated at
        entry_list = Semester.find_entry_debater_id(self.debater_id)

        # Populating self.tour_attended
        # Cycle through every entry and assign every key as "tournament date" and the value as points
        for entry in entry_list:
            tournament = entry['tournament']
            service = entry['service']
            judging = entry['judging']
            date = entry['semester']
            points = entry['points']

            # Determining whether the tournament was judge, service or debater
            if judging:
                self.tour_attended[tournament + ' ' + date + ' (Judging)'] = points

            elif service:
                self.tour_attended['Service ' + date] = points

            else:
                self.tour_attended[tournament + ' ' + date] = points

    def __str__(self) -> str:
        """
        String representation of debater instance
        Will return Name, debater id, and tournament list. ie.

        Name: Ameen Parthab
        id: 1
        Tournaments attended
        WUDC Fall 2019 > 50
        HWS RR Winter 2020 > 40

        """

        return (
                'Name: ' + self.name + '\n' +
                'id: ' + str(self.debater_id) + '\n' +
                'Tournaments attended: \n' +
                self.return_tournaments()
        )

    def return_tournaments(self) -> str:
        """ Return all tournaments attended """
        return_str = ''

        for tour in self.tour_attended:
            return_str = return_str + tour + ' > ' + self.tour_attended[tour] + '\n'

        return return_str

    def last_four_semester(self) -> List[str]:
        """
        Return the last 4 semesters a debater has debated in.
        """





    def get_top_five_sem(self, semester: str) -> int:
        """
        Return the total points from a debaters top 5 tournaments attended that semester
        Note this only includes at max 3 competitive tournaments.
        """
        sem_txt = semester + ".json"
        sem = Semester(semester, sem_txt)
        tourn_counter = 0  # Keeps count of total tournaments up to 5
        comp_tourn = 0  # Keeps count of total competitive tournaments up to 3
        points = 0

        entry_list = sem.find_entry_debater_id(self.debater_id)
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

    def calculate_service_points_sem(self, semester: str) -> int:
        """
        Calculate a debaters service points in one semester
        """
        sem_txt = semester + ".json"
        sem = Semester(semester, sem_txt)
        entry_list = sem.find_entry_debater_id(self.debater_id)

        filtered_entry_list = []

        # Creating the filtered list one tournament at a time
        for entry in entry_list:
            if entry['service']:
                filtered_entry_list.append(entry)

        service_points = 0
        for entry in filtered_entry_list:
            if semester == entry['date']:
                service_points += entry['points']

        return service_points

    def calculate_service_points(current_sem: str, self):
        four_semesters = self.last_four_semester()
        three_semesters = four_semesters[0:3]



    def calculate_comp_points(self, debater_id: int) -> int:
        pass

    def calculate_total_points(self, debater_id: int) -> int:
        """
        Calculate a debaters total relevant points
        """

        return (self.calculate_comp_points(debater_id)
                + self.calculate_service_points(debater_id))
