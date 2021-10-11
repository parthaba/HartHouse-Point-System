from Classes import Extract


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
        entry_list = Extract.find_entry_debater_id(self.debater_id)

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

    def last_four_semester(self, debater_id: int) -> List[str]:
        """
        Return the last 4 semesters a debater has debated in.
        """

        entry_list = self.find_entry_debater_id(debater_id)
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
