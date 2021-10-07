from typing import List, Dict
from Classes.Team import Team
from Classes.TeamMaker import TeamMaker


class Qualifier:
    """A class for handling tournament qualifiers. Can handle non-tryout qualifiers
    independently.

    Instance Attributes:
        - teams: a list of teams attending the qualifier (and the respective debater IDs
                 of each debater)
        - number_of_teams: the number of teams that are participating in the qualifier
        - limit: number of spots available
        - team_points: the working point total of each team
        - team_ranks: list of teams sorted from highest points to lowest points

    Representation Invariants:
        - all IDs in self.teams are valid IDs
        - no IDs are repeated in self.teams
        - len(teams) > limit
        - number_of_teams > 0
        - limit > 0
    """
    teams: List[Team]
    number_of_teams: int
    limit: int
    team_points: Dict[Team, float]
    team_ranks: List[Team]

    def __init__(self, number_of_teams: int, limit: int) -> None:
        """Initialize a qualifier."""
        self.number_of_teams = number_of_teams
        self.limit = limit
        self.team_points = {}
        self.team_ranks = []

        # Instantiate self.teams, self._team_points, and self._team_ranks
        self.teams = self.make_teams()
        self.compile_teams()

    def make_teams(self) -> List[Team]:
        """Create Team objects to populate self.teams"""
        team_maker = TeamMaker(self.limit)
        return team_maker.create_team_list()

    def compile_teams(self) -> None:
        """Update _team_points and _team_ranks."""
        for team in self.teams:
            self.team_points[team] = team.working_point_total

        # Sort teams from highest to lowest based on working point totals
        self.team_ranks = sorted(self.teams, key=lambda x: x.working_point_total, reverse=True)

    def display_qualifying_teams(self) -> None:
        """Display the teams that receive spots for the tournament."""
        qualifying_teams = self.team_ranks[:self.limit]

        for team in qualifying_teams:
            print(team.team_name + "\n")

        print(self.team_ranks)



