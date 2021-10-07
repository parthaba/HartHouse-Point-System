from Classes.Team import Team
from Classes.Debater import Debater
from typing import List


class TeamMaker:
    """Creates a list of teams.

    Instance attributes:
        - team_list: a list of tuples. each tuple contains two debater ids
        - number_of_teams: the number of teams competing in the qualifier

    Representation invariants:
        - len(team_list) >= 0
        - number_of_teams >= 0
    """
    team_list: List[List[int]]
    number_of_teams: int

    def __init__(self, number_of_teams):
        """Construct a new TeamMaker object."""
        self.team_list = []
        self.number_of_teams = number_of_teams
        self.create_team_ids()

    def create_team_ids(self) -> None:
        """Fill the team_list attribute."""
        current_team = 1
        for x in range(self.number_of_teams):
            x = int(input("Input debater id of first debater in the format <id_1> "
                          "for team " + str(current_team) + "."))
            y = int(input("Input debater id of second debater in the format <id_2> "
                          "for team " + str(current_team) + "."))

            current_team += 1
            self.team_list.append([x, y])

        if len(self.team_list) == self.number_of_teams:
            print("Teams added!")

    def create_team_list(self) -> List[Team]:
        """Create a list of team objects."""
        list_of_teams_so_far = []
        for team_ids in self.team_list:
            # Creating two debater objects
            debater1 = Debater(team_ids[0])
            debater2 = Debater(team_ids[1])

            names = [debater1.name, debater2.name]
            # TODO: figure out how to parse the last names from each name
            team_name = "lebron"

            new_team = Team(team_ids, names, team_name)
            list_of_teams_so_far.append(new_team)

        return list_of_teams_so_far
