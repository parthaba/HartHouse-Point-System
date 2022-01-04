from typing import List, Dict
from Classes.Team import Team
from Classes.TeamMaker import TeamMaker


class Qualifier:
    """A class for handling tournament qualifiers. Can handle non-tryout qualifiers
    independently. There are two ways to add teams: populate_qualifier_textUI and set_team_list.

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

    def set_team_list(self, team_list: List[List[int]]) -> None:
        """Set self.teams using a list of debater IDs"""
        new_qual = TeamMaker(self.number_of_teams)
        new_qual.team_list = team_list
        self.teams = new_qual.create_team_list()
        self.compile_teams()

    def populate_qualifier_text_UI(self) -> None:
        """Make teams and compile everything for the qualifier."""
        # Instantiate self.teams, self._team_points, and self._team_ranks
        self.teams = self.make_teams()
        self.compile_teams()

    def __str__(self):
        """Display string of qualifier."""
        team_string = ''
        for team in self.team_ranks:
            team_string = team_string + team.team_name + ": " + str(team.working_point_total) + "\n"

        return team_string

    def make_teams(self) -> List[Team]:
        """Create Team objects to populate self.teams"""
        team_maker = TeamMaker(self.number_of_teams)
        team_maker.create_team_ids()
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
