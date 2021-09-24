from typing import List


class Qualifier:
    """A parent class for handling tournament qualifiers.

    Instance Attributes:
        - teams: a list of teams attending the qualifier (and the respective debater IDs
                 of each debater)
        - limit: number of spots available

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

    def compile_team_points(self) -> None:
        """Update _team_points."""

class Tryout_Qualifier(Qualifier):
    """A subclass of the Qualifier parent class for qualifiers that require a tryout (rounds)."""
