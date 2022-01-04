from typing import List
from Classes.Debater import Debater


class Team:
    """A class that represents a single debate team in a qualifier.

    Instance Attributes:
        - debater_ids: the debater ids of each debater on the team (only two debaters per team)
        - debater_names: the names of each debater, respectively (same index)
        - team_name: the name of the team for the purposes of the qualifier
        - combined points: the number of points this team has

    Representation Invariants
        - debater_ids != ()
        - len(debater_ids) == 2
        - debater_names != ()
        - len(debater_names) == 2
        - team_name != ''
        - combined points >= 0
    """
    debater_ids: List[int]
    debater_names: List[str]
    team_name: str
    working_point_total: float

    def __init__(self, ids: List[int], names: List[str], team_name: str):
        """Constructor for the team class."""
        self.debater_ids = ids
        self.debater_names = names
        self.team_name = team_name
        self.working_point_total = self.calculate_points()

    def calculate_points(self) -> float:
        """Calculate the total number of working points for this team."""
        return sum([Debater(debater_id).working_points for debater_id in self.debater_ids])
