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

