from typing import List


class Qualifier:
    """A parent class for handling tournament qualifiers.

    Instance Attributes:
        - teams: a list of teams attending the qualifier (and the respective debater IDs
                 of each debater)
        - limit: number of spots available
        - rounds: number of rounds held at the tryout
        - rooms: number of rooms

    Representation Invariants:
        - all IDs in self.teams are valid IDs
        - no IDs are repeated in self.teams
        - self.teams.length > limit
        - limit > 0
    """
    teams: List[list]
    limit: int

    # Private Instance Attributes:
    #   - _team_points: the respective competitive points sum of each team
    #   - _team_ranks: list of teams sorted from highest points to lowest points
    _team_points: dict
    _team_ranks: list

    def __init__(self, teams: List[list], limit: int) -> None:
        """Initialize a qualifier."""
        self.teams = teams
        self.limit = limit
        self._team_points = {}
        self._team_ranks = []

    def compile_teams(self) -> None:
        """Update _team_points and _team_ranks."""

    def compile_team_points(self) -> None:
        """Update _team_points."""


class TryoutQualifier(Qualifier):
    """A subclass of the Qualifier parent class for qualifiers that require a tryout (rounds).

    Instance Attributes:
        - rounds: number of rounds held at the tryout
        - rooms: number of rooms

    Representation
    """
    rounds: int
    rooms: int
    field: float

    # Private Instance Attributes:
    #   - _max_points: maximum number of debate points a team can get at the tryout
    _max_points = 0

    def __init__(self, teams: List[list], limit: int, rounds: int, rooms: int) -> None:
        super().__init__(teams, limit)
        self.max_points = rounds * 3
        self.rooms = rooms
        self.field = self.determine_field()

        self.compile_teams()
        self.compile_team_points()

    def pre_tryout(self):
        """Display the pre-tryout rankings and qualification requirements for each team.

        steps:
        - compile teams
        - determine the worth of each point (field/maximum)
        - show what each team needs to do to qualify"""

        Qualifier.compile_teams(self)

    def determine_field(self):
        """Determine the field for this qualifier."""
        sum_top_teams = 0

        for x in range(self.limit):
            sum_top_teams += self._team_points[self._team_ranks[x]]

        return sum_top_teams / len(self.teams)

    def identify_baller_teams(self, team: int) -> bool:
        """Determine which team(s) qualify for the tournament regardless of how
        they do in the qualifier."""

        baller_team_points = self._team_points[self.teams[team]]

        # In order for team to not qualify, self.limit other teams would have to rank above them in competitive
        # points after the tryout is over. If that is impossible given the points of the other team, team will
        # qualify no matter what.
        total_gap = 0
        for current_team in self.teams[1:self.limit]:
            current_team_points = self._team_points[current_team]
            gap = baller_team_points - current_team_points
            total_gap += gap

        biggest_possible_gap = self.rooms * 3 * self.field
        return total_gap > biggest_possible_gap


