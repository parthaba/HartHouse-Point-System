from Classes.Team import Team
from Classes.Debater import Debater
from typing import List


class TeamMaker:
    """Creates a list of teams.

    Instance attributes:
        - team_list: a list of lists. each inner list contains two debater ids
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

    def create_team_ids(self) -> None:
        """Fill the team_list attribute."""
        current_team = 1
        for x in range(self.number_of_teams):
            debater_one = int(input("Input debater id of first debater in the format <id_1> "
                          "for team " + str(current_team) + "."))
            print(Debater(debater_one).name)

            debater_two = int(input("Input debater id of second debater in the format <id_2> "
                          "for team " + str(current_team) + "."))
            print(Debater(debater_two).name)

            current_team += 1
            self.team_list.append([debater_one, debater_two])

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
            team_name = names[0] + " & " + names[1]

            new_team = Team(team_ids, names, team_name)
            list_of_teams_so_far.append(new_team)

        return list_of_teams_so_far
